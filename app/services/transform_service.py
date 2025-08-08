from PIL import Image, ImageFilter, ImageOps, ImageColor
from app.storage import get_storage_adapter
import io
import os

storage = get_storage_adapter()

def process_image_on_the_fly(image_id, params):
    """
    Fetches an original image, applies transformations in memory,
    and returns the raw image data and its MIME type.
    """
    # 1. Fetch original image data from storage
    original_image_data = storage.read(image_id)
    if original_image_data is None:
        raise FileNotFoundError("Original image not found in storage.")

    img = Image.open(io.BytesIO(original_image_data))
    
    # Preserve original format for saving later
    original_format = img.format or 'PNG'
    # Ensure image is in a mode that supports transparency for pasting
    img = img.convert("RGBA")

    # 2. Apply transformations in a specific order
    
    # Step A: Perfect Fit (Trim whitespace and add uniform padding)
    if params.get('perfect_fit') is not None:
        padding = params.get('perfect_fit')
        
        # Trim whitespace by getting the bounding box of non-alpha pixels
        bbox = img.getbbox()
        if bbox:
            img = img.crop(bbox)
        
        # Create a new transparent canvas with the padding included
        new_size = (img.width + 2 * padding, img.height + 2 * padding)
        padded_img = Image.new("RGBA", new_size, (0, 0, 0, 0))
        padded_img.paste(img, (padding, padding))
        
        # The trimmed and padded image is now our base image
        img = padded_img

    # Step B: Standard resizing and cropping
    if params.get('w') or params.get('h'):
        width = params.get('w')
        height = params.get('h')
        fit = params.get('fit', 'contain')

        if not width: width = height if height else img.width
        if not height: height = width if width else img.height
        
        if fit == 'crop':
            img = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
        else: # Default to 'contain'
            img.thumbnail((width, height), Image.Resampling.LANCZOS)

    # Step C: Canvas Padding
    if params.get('pad_w') and params.get('pad_h'):
        pad_w = params.get('pad_w')
        pad_h = params.get('pad_h')
        pad_color = params.get('pad_color', 'white')

        try:
            background = Image.new('RGBA', (pad_w, pad_h), ImageColor.getcolor(pad_color, "RGBA"))
        except ValueError:
            background = Image.new('RGBA', (pad_w, pad_h), (255, 255, 255, 255))

        paste_x = (pad_w - img.width) // 2
        paste_y = (pad_h - img.height) // 2
        
        background.paste(img, (paste_x, paste_y), img)
        img = background

    # Step D: Filters are applied last
    if params.get('filter') == 'grayscale':
        img = ImageOps.grayscale(img).convert("RGBA")
    elif params.get('filter') == 'sepia':
        sepia_img = img.convert("L")
        sepia_palette = []
        r, g, b = (255, 240, 192)
        for i in range(256):
            sepia_palette.extend((int(r*i/255), int(g*i/255), int(b*i/255)))
        sepia_img.putpalette(sepia_palette)
        img = sepia_img.convert("RGB").convert("RGBA")

    if params.get('blur'):
        blur_radius = min(params.get('blur'), 50)
        img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # 3. Save transformed image to an in-memory buffer
    buffer = io.BytesIO()
    final_format = 'PNG' if img.mode == 'RGBA' else original_format
    img.save(buffer, format=final_format)
    buffer.seek(0)

    mime_type = Image.MIME.get(final_format.upper(), 'image/png')
    return buffer.getvalue(), mime_type
