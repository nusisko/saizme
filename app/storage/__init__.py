from app.config import Config
from .gcs_adapter import GoogleCloudStorageAdapter
from .local_adapter import LocalStorageAdapter

def get_storage_adapter():
    provider = Config.STORAGE_PROVIDER
    if provider == "gcs":
        print("Selected storage provider: Google Cloud Storage")
        return GoogleCloudStorageAdapter()
    else:
        print("Selected storage provider: Local")
        return LocalStorageAdapter()