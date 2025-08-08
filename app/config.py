import os
from dotenv import load_dotenv

# Find the absolute path of the project's root directory
# This navigates up two levels from the current file (app/config.py)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Load the .env file from the project root
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    """Holds all configuration for the application."""
    STORAGE_PROVIDER = os.getenv("STORAGE_PROVIDER", "local")
    GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME")
    GCS_CREDENTIALS_PATH = os.path.join(BASE_DIR, 'credentials', 'gcs-key.json')
