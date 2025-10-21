import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv
import re
import json

load_dotenv()
LOCATIONIQ_TOKEN = os.getenv("LOCATIONIQ_TOKEN")

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"]}})

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
        print(f"Data parsing error for {city_name} from external APIs: {e}")
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
        return jsonify({"error": "Invalid search query"}), 400

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

if __name__ == "__main__":
    app.run(port=5001, debug=True)