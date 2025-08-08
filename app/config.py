import os
from dotenv import load_dotenv

# Load variables from .env file into environment
load_dotenv()

class Config:
    """Holds all configuration for the application."""
    STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER", "local")
    GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
    GCS_CREDENTIALS_PATH = "/app/credentials/gcs-key.json"