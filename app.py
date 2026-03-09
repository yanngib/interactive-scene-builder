import base64
import os
from flask import Flask, render_template, request, jsonify
import google.auth
import vertexai
from vertexai.vision_models import Image, ImageGenerationModel

app = Flask(__name__, template_folder='.')

# --- Initialize Vertex AI ---
# This is now done once when the app starts.
try:
    # Attempt to get project ID and location from the environment
    # By explicitly requesting the cloud-platform scope, we ensure the credentials are valid for Vertex AI.
    credentials, PROJECT_ID = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    LOCATION = "us-central1" # Most models are available here
    vertexai.init(project=PROJECT_ID, location=LOCATION, credentials=credentials) # Explicitly pass credentials

    print(f"✅ Vertex AI initialized successfully for project: {PROJECT_ID}")
except Exception as e:
    print("❌ ERROR: Failed to initialize Vertex AI.")
    print("   - Have you enabled the 'aiplatform.googleapis.com' API for your project?")
    print(f"   - Details: {e}")
    PROJECT_ID = None # Set to None to indicate initialization failure

@app.route('/')
def index():
    """Renders the main page which contains the React application."""
    return render_template('index.html')

@app.route('/generate-image', methods=['POST'])
def generate_image():
    """
    Handles a POST request to generate an image from a text prompt using Imagen.
    """
    data = request.get_json()
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({'error': 'Prompt is required'}), 400

    if not PROJECT_ID:
        # If initialization failed at startup, don't even try.
        return jsonify({'error': 'Vertex AI is not configured on the server.'}), 503

    try:
        model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")
        images = model.generate_images(
            prompt=f"A simple, single, isolated object on a plain background: {prompt}",
            number_of_images=1
        )
        image_bytes = images[0]._image_bytes
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        return jsonify({'image_data': f'data:image/png;base64,{base64_image}'})
    except Exception as e:
        print(f"❌ An error occurred during image generation: {e}")
        return jsonify({'error': 'Image generation failed on the server.', 'details': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)