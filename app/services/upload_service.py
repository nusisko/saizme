from werkzeug.utils import secure_filename
from app.storage import get_storage_adapter
import uuid
import os

storage = get_storage_adapter()

def save_original_image(file):
    """Saves the original uploaded image and returns a unique ID."""
    filename = secure_filename(file.filename)
    unique_id = f"original-image-{uuid.uuid4()}{os.path.splitext(filename)[1]}"
    
    file_data = file.read()
    storage.save(file_data, unique_id)
    
    return unique_id
