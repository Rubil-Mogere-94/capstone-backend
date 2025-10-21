# Capstone Backend

This is the backend for the Capstone project, built with Flask.

## Deployment on Render

This backend is designed to be deployed on Render. Follow these steps:

1.  **Create a new Web Service on Render:**
    *   Connect your GitHub repository containing this backend code.
    *   Select "Python" as the runtime.
2.  **Build Command:**
    `pip install -r requirements.txt`
3.  **Start Command:**
    `gunicorn app:app`
4.  **Environment Variables:**
    *   Set the `LOCATIONIQ_TOKEN` environment variable in the Render dashboard. This token is crucial for the LocationIQ API.
    *   Any other environment variables defined in your local `.env` file should also be added to Render's environment settings.

## Local Development

1.  **Create a virtual environment:**
    `python3 -m venv venv`
2.  **Activate the virtual environment:**
    `source venv/bin/activate`
3.  **Install dependencies:**
    `pip install -r requirements.txt`
4.  **Create a `.env` file:**
    Create a file named `.env` in the `backend` directory and add your `LOCATIONIQ_TOKEN` (and any other necessary environment variables) to it:
    ```
    LOCATIONIQ_TOKEN="your_locationiq_token_here"
    ```
5.  **Run the application:**
    `flask run --port 5001`
