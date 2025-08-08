from google.cloud import storage
from app.config import Config
from .interface import StorageInterface
import os
from typing import Optional

class GoogleCloudStorageAdapter(StorageInterface):
    def __init__(self):
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = Config.GCS_CREDENTIALS_PATH
        self.storage_client = storage.Client()
        self.bucket_name = Config.GCS_BUCKET_NAME
        self.bucket = self.storage_client.bucket(self.bucket_name)
        print("Initializing Google Cloud Storage adapter.")

    
    def save(self, file_data, filename):
        blob = self.bucket.blob(f"uploads/{filename}")
        blob.upload_from_string(file_data)
        return blob.public_url

    def read(self, object_name: str) -> Optional[bytes]:
        try:
            blob = self.bucket.blob(f"uploads/{object_name}")
            return blob.download_as_bytes()
        except Exception:
            return None