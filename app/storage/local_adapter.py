import os
from .interface import StorageInterface

class LocalStorageAdapter(StorageInterface):
    def __init__(self):
        self.upload_folder = "local_uploads"
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)
        print("Initializing Local Storage adapter.")

    def save(self, file_data, filename):
        path = os.path.join(self.upload_folder, filename)
        with open(path, "wb") as f:
            f.write(file_data)
        return f"File saved locally to: {path}"

    def read(self, filename):
        path = os.path.join(self.upload_folder, filename)
        try:
            with open(path, "rb") as f:
                return f.read()
        except FileNotFoundError:
            return None