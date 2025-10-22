import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import re
import json
from functools import wraps

# Firebase Admin SDK imports
import firebase_admin
from firebase_admin import credentials, firestore, auth

load_dotenv()
LOCATIONIQ_TOKEN = os.getenv("LOCATIONIQ_TOKEN")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

# --- Firebase Admin SDK Initialization ---
db = None
try:
    # Prioritize environment variable for service account key
    firebase_service_account_key_json = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    if firebase_service_account_key_json:
        # If it's a JSON string, parse it
        cred = credentials.Certificate(json.loads(firebase_service_account_key_json))
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized using environment variable.")
    elif os.path.exists("serviceAccountKey.json"):
        # Fallback to local file for development
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred)
        print("Firebase Admin SDK initialized using serviceAccountKey.json.")
    else:
        print("Firebase Admin SDK not initialized: No service account key found.")
except Exception as e:
    print(f"Error initializing Firebase Admin SDK: {e}")

if firebase_admin._apps: # Check if app was initialized
    db = firestore.client()
    print("Firestore client initialized.")
else:
    print("Firestore client not initialized because Firebase Admin SDK failed to initialize.")

# --- Firebase ID Token Verification Middleware ---
def verify_firebase_token(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not firebase_admin._apps:
            return jsonify({"message": "Firebase Admin SDK not initialized."}), 500

        id_token = request.headers.get('Authorization')
        if not id_token:
            return jsonify({"message": "Authorization token required"}), 401
        
        # Expecting "Bearer <token>"
        if id_token.startswith('Bearer '):
            id_token = id_token.split('Bearer ')[1]
        else:
            return jsonify({"message": "Invalid Authorization header format"}), 401

        try:
            decoded_token = auth.verify_id_token(id_token)
            request.uid = decoded_token['uid']
            return f(*args, **kwargs)
        except Exception as e:
            print(f"Firebase token verification failed: {e}")
            return jsonify({"message": "Invalid or expired token"}), 403
    return decorated_function

def get_wikipedia_summary(title):
    try:
        wikipedia_url = f"https://en.wikipedia.org/w/api.php?action=query&format=json&prop=extracts&exintro&explaintext&redirects=1&titles={title}"
        headers = {'User-Agent': 'CapstoneFrontend/1.0'}
        response = requests.get(wikipedia_url, headers=headers)
        response.raise_for_status()
        data = response.json()

        page = next(iter(data['query']['pages'].values()), None)
        if page and 'extract' in page:
            return page['extract']
        return None
    except requests.exceptions.RequestException as e:
        print(f"Network or API error fetching Wikipedia summary for {title}: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred fetching Wikipedia summary for {title}: {e}")
        return None

def get_destination_details(city_name):
    try:
        headers = {'User-Agent': 'CapstoneFrontend/1.0'} # Custom User-Agent
        nominatim_url = f'https://nominatim.openstreetmap.org/search?q={city_name}&format=json&limit=1'
        nominatim_response = requests.get(nominatim_url, headers=headers)
        nominatim_response.raise_for_status()
        nominatim_res = nominatim_response.json()

        if not nominatim_res or not isinstance(nominatim_res, list) or len(nominatim_res) == 0:
            print(f"Nominatim API returned no results or unexpected format for {city_name}")
            return None

        # Check if the first result has the expected keys
        if 'lat' not in nominatim_res[0] or 'lon' not in nominatim_res[0]:
            print(f"Nominatim API result missing 'lat' or 'lon' for {city_name}")
            return None

        lat = nominatim_res[0]['lat']
        lon = nominatim_res[0]['lon']

        details = {
            "id": city_name,
            "name": city_name,
            "lat": float(lat),
            "lon": float(lon),
        }

        # Fetch Wikipedia summary
        wikipedia_summary = get_wikipedia_summary(city_name)
        if wikipedia_summary:
            details["description"] = wikipedia_summary
        
        return details

    except requests.exceptions.RequestException as e:
        print(f"Network or API error fetching details for {city_name}: {e}")
        return None
    except (KeyError, IndexError) as e:
        print(f"Data parsing error for {city_name} from external APIs: {e}. Response might be malformed or missing expected keys.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred fetching details for {city_name}: {e}")
        return None

def validate_search_query(query):
    if not query or len(query) > 100:
        return False
    # Allow alphanumeric characters, spaces, commas, and hyphens
    return bool(re.match(r'^[a-zA-Z0-9\s,\-]+$', query))

@app.route("/api/search", methods=["GET"])
def search_destinations():
    query = request.args.get('q', '').strip()

    if not validate_search_query(query):
        return jsonify({"error": "Invalid search query. Query must be alphanumeric, spaces, commas, or hyphens, and less than 100 characters."}), 400

    details = get_destination_details(query)
    if details:
        return jsonify([details])
    else:
        return jsonify([])

@app.route("/api/location/search", methods=["GET"])
def location_search():
    query = request.args.get('q')
    token = os.getenv("LOCATIONIQ_TOKEN")

    headers = {'User-Agent': 'CapstoneFrontend/1.0'} # Custom User-Agent
    response = requests.get(
        f'https://us1.locationiq.com/v1/search.php?key={token}&q={query}&format=json',
        headers=headers
    )
    return jsonify(response.json())

@app.route("/api/location/search", methods=["GET"])
def location_search():
    query = request.args.get('q')
    token = os.getenv("LOCATIONIQ_TOKEN")

    headers = {'User-Agent': 'CapstoneFrontend/1.0'} # Custom User-Agent
    response = requests.get(
        f'https://us1.locationiq.com/v1/search.php?key={token}&q={query}&format=json',
        headers=headers
    )
    return jsonify(response.json())

# --- User Preferences API Endpoints ---
@app.route("/api/user/preferences", methods=["GET"])
@verify_firebase_token
def get_user_preferences():
    if not db:
        return jsonify({"message": "Firestore client not available."}), 500
    
    uid = request.uid
    doc_ref = db.collection('user_preferences').document(uid)
    doc = doc_ref.get()

    if doc.exists:
        return jsonify(doc.to_dict()), 200
    else:
        return jsonify({}), 200 # Return empty object if no preferences found

@app.route("/api/user/preferences", methods=["POST", "PUT"])
@verify_firebase_token
def update_user_preferences():
    if not db:
        return jsonify({"message": "Firestore client not available."}), 500

    uid = request.uid
    data = request.get_json()

    if not data:
        return jsonify({"message": "Request body must be JSON"}), 400

    doc_ref = db.collection('user_preferences').document(uid)
    try:
        doc_ref.set(data, merge=True)
        return jsonify({"message": "Preferences updated successfully"}), 200
    except Exception as e:
        print(f"Error updating user preferences for {uid}: {e}")
        return jsonify({"message": "Failed to update preferences"}), 500

# --- Conceptual Recent Activity API Endpoint ---
@app.route("/api/user/activity", methods=["GET"])
@verify_firebase_token
def get_user_activity():
    # This is a placeholder for future functionality
    mock_activity_data = [
        {"id": "1", "type": "destination_view", "details": "Paris", "timestamp": "2025-10-22T10:00:00Z"},
        {"id": "2", "type": "preference_update", "details": "Theme changed to dark", "timestamp": "2025-10-22T09:30:00Z"},
    ]
    return jsonify(mock_activity_data), 200

@app.route("/")
def hello():
    return "Hello from the backend!"

if __name__ == "__main__":
    app.run(port=5001, debug=True)