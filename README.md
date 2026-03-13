# Interactive Scene Builder with Vertex AI

This project is a web-based application that allows users to interactively build scenes by generating individual objects and then composing them into a final, artistic rendering. It uses a Flask backend to serve a frontend application and communicates with Google Cloud's Vertex AI to generate images using the Imagen 3.0 model.

## Features

*   **Object Generation**: Generate images of single, isolated objects from a simple text prompt (e.g., "a red chair", "a tall tree").
*   **Scene Rendering**: Generate a complete, vibrant, and colorful illustration of a scene from a detailed description that includes the previously generated objects.
*   **Web Interface**: A simple frontend (served via `index.html`) to interact with the image generation APIs.
*   **Scalable Backend**: Built with Flask and designed to run in a containerized environment like Google Cloud Run or Cloud Shell.

## Architecture

The application consists of a single Python backend service:

*   **`app.py` (Flask Server)**:
    *   Initializes the Vertex AI SDK with credentials from the environment.
    *   Serves the main `index.html` page.
    *   Provides two API endpoints for image generation:
        *   `/generate-image`: For creating individual objects.
        *   `/render-scene`: For creating the final composite scene.

## Prerequisites

*   Python 3.7+
*   A Google Cloud Project.
*   The `gcloud` CLI installed and authenticated.
*   The Vertex AI API (`aiplatform.googleapis.com`) enabled in your Google Cloud project.

## Setup

1.  **Clone the Repository**
    ```bash
    # If this is in a git repository
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```

2.  **Install Dependencies**
    It's recommended to use a virtual environment.
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install Flask "google-cloud-aiplatform>=1.38" google-auth
    ```

3.  **Enable Google Cloud API**
    Make sure the Vertex AI API is enabled for your project.
    ```bash
    gcloud services enable aiplatform.googleapis.com --project=<YOUR_PROJECT_ID>
    ```

4.  **Authentication**
    The application uses Application Default Credentials (ADC) to authenticate with Google Cloud services.

    *   **Local Development**: Authenticate your local environment.
        ```bash
        gcloud auth application-default login
        ```
    *   **Cloud Shell / GCE / Cloud Run**: No extra steps are needed. The environment is automatically authenticated.

## Running the Application

1.  **Start the Flask Server:**
    ```bash
    python3 app.py
    ```
    The server will start on `http://0.0.0.0:8080`.

2.  **Access the Application:**
    *   **Locally**: Open your browser and navigate to `http://localhost:8080`.
    *   **Cloud Shell**: Use the "Web Preview" feature in Cloud Shell and select port 8080 to open the application in a new tab.

## API Endpoints

The backend provides the following RESTful endpoints:

*   `POST /generate-image`
    *   **Description**: Generates an image of a single object.
    *   **Body**: `{"prompt": "a description of the object"}`
*   `POST /render-scene`
    *   **Description**: Renders a full scene.
    *   **Body**: `{"prompt": "a detailed description of the final scene"}`

Both endpoints return a JSON object with the base64-encoded image data: `{"image_data": "data:image/png;base64,..."}`.