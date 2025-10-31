# Capstone Backend

This is the backend for the Capstone project, built with Flask. It provides a RESTful API for managing user preferences, searching for destinations, and a community forum.

## Features

-   **User Preferences:** Users can save and update their application preferences.
-   **Destination Search:** Search for destinations using LocationIQ and get details from Wikipedia and OpenStreetMap.
-   **Community Forum:** A forum for users to create posts and comment on them.
-   **Authentication:** User authentication is handled by Firebase Authentication.

## Technologies Used

-   **Framework:** Flask
-   **Database:** PostgreSQL for the community forum and Firebase Firestore for user preferences.
-   **Authentication:** Firebase Authentication
-   **APIs:**
    -   LocationIQ for location search.
    -   Wikipedia for destination descriptions.
    -   OpenStreetMap for destination coordinates.

## Getting Started

### Prerequisites

-   Python 3
-   pip
-   A running PostgreSQL instance.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Rubil-Mogere-94/capstone-backend.git
    cd capstone-backend
    ```

2.  **Create a virtual environment and activate it:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install the dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Create a `.env` file in the root of the project and add the following environment variables:

```
LOCATIONIQ_TOKEN="your_locationiq_token_here"
FIREBASE_SERVICE_ACCOUNT_KEY="your_firebase_service_account_key_as_json"
DATABASE_URL="postgresql://user:password@localhost/mydatabase"
```

-   `LOCATIONIQ_TOKEN`: Your API token from [LocationIQ](https://locationiq.com/).
-   `FIREBASE_SERVICE_ACCOUNT_KEY`: The JSON content of your Firebase service account key.
-   `DATABASE_URL`: The connection string for your PostgreSQL database.

### Running the Application

1.  **Create the database tables:**
    The application will automatically create the necessary tables in your PostgreSQL database when it starts.

2.  **Run the application:**
    ```bash
    flask run --port 5001
    ```
    The application will be available at `http://127.0.0.1:5001`.

## API Endpoints

### Authentication

All protected endpoints require an `Authorization` header with a Firebase ID token:

```
Authorization: Bearer <firebase_id_token>
```

### Community Forum

-   `GET /api/forum/posts`: Get all posts.
-   `POST /api/forum/posts`: Create a new post (requires authentication).
-   `GET /api/forum/posts/<post_id>/comments`: Get all comments for a post.
-   `POST /api/forum/posts/<post_id>/comments`: Create a new comment for a post (requires authentication).
-   `DELETE /api/forum/posts/<post_id>`: Delete a post (requires authentication).

### Destinations

-   `GET /api/search?q=<query>`: Search for a destination.
-   `GET /api/location/search?q=<query>`: Search for a location using LocationIQ.

### User

-   `GET /api/user/preferences`: Get the current user's preferences (requires authentication).
-   `POST /api/user/preferences`: Create or update the current user's preferences (requires authentication).
-   `PUT /api/user/preferences`: Update the current user's preferences (requires authentication).
-   `GET /api/user/activity`: Get the current user's activity (mock data).

## Project Structure

```
.
├── .env                  # Environment variables
├── app.py                # Main Flask application
├── README.md             # This file
├── requirements.txt      # Python dependencies
└── __pycache__/          # Python cache
```
