from google.cloud import aiplatform_v1beta1
from google.cloud.aiplatform_v1beta1.types import PredictRequest
from google.oauth2 import service_account
import base64

# Replace with your values
PROJECT_ID = "dreamscriptor-b6416"
LOCATION = "us-central1"
SERVICE_ACCOUNT_FILE = "dreamscriptor.json"  # <- Put the real path here

# Setup client
credentials = service_account.Credentials.from_service_account_file("dreamscriptor.json")
client = aiplatform_v1beta1.PredictionServiceClient(credentials=credentials)

def generate_imagen2_image(prompt: str):
    endpoint = f"projects/{PROJECT_ID}/locations/{LOCATION}/publishers/google/models/imagegeneration@006"

    instance = {"prompt": prompt, "sampleCount": 1, "imageSize": "1024x1024"}
    request = PredictRequest(endpoint=endpoint, instances=[instance])

    response = client.predict(request=request)
    image_base64 = response.predictions[0]["bytesBase64"]

    image_url = f"data:image/png;base64,{image_base64}"  # You can show this directly in Streamlit
    return image_url
