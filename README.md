# Capstone Backend

This is the backend for the Capstone project, built with Flask.

## Getting Started

### Prerequisites

*   Python 3
*   pip

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/Rubil-Mogere-94/capstone-backend.git
    ```
2.  Install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Environment Variables

Create a `.env` file in the root of the project and add the following environment variables:

```
LOCATIONIQ_TOKEN="your_locationiq_token_here"
FIREBASE_SERVICE_ACCOUNT_KEY="your_firebase_service_account_key_here"
```

### Running the Application

```bash
flask run --port 5001
```