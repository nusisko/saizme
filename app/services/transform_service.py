from PIL import Image, ImageFilter, ImageOps, ImageColor
from app.storage import get_storage_adapter
import io

# Initialize the storage adapter once for this service
storage = get_storage_adapter()

def process_image_on_the_fly(image_id: str, params: dict):
    """
    Fetches an original image from storage, applies a series of transformations
    in memory based on the provided parameters, and returns the final raw
    image data along with its MIME type.
    """
    # 1. Fetch original image data from storage
    original_image_data = storage.read(image_id)
    if original_image_data is None:
        raise FileNotFoundError(f"Image '{image_id}' not found in storage.")

    img = Image.open(io.BytesIO(original_image_data))
    
    # Preserve original format for saving later
    original_format = img.format or 'PNG'
    # Ensure image is in a mode that supports transparency for all operations
    img = img.convert("RGBA")

    # 2. Apply transformations in a specific order
    
    # Step A: Perfect Fit
    if 'perfect_fit' in params:
        padding = params.get('perfect_fit', 0)
        bbox = img.getbbox()
        if bbox:
            trimmed_img = img.crop(bbox)
            new_size = (trimmed_img.width + 2 * padding, trimmed_img.height + 2 * padding)
            padded_img = Image.new("RGBA", new_size, (0, 0, 0, 0))
            padded_img.paste(trimmed_img, (padding, padding))
            img = padded_img

    # Step B: Sizing, Cropping, and Background
    if params.get('w') or params.get('h'):
        width = params.get('w')
        height = params.get('h')
        fit = params.get('fit', 'contain')

        if not width: width = height
        if not height: height = width
        
        if fit == 'crop':
            img = ImageOps.fit(img, (width, height), Image.Resampling.LANCZOS)
        else: # 'contain'
            bg_color_str = params.get('bg_color', 'transparent')
            try:
                background_color = (0,0,0,0) if bg_color_str == 'transparent' else ImageColor.getcolor(bg_color_str, "RGBA")
            except ValueError:
                background_color = (0,0,0,0)

            background = Image.new('RGBA', (width, height), background_color)
            img_copy = img.copy()
            img_copy.thumbnail((width, height), Image.Resampling.LANCZOS)
            paste_x = (width - img_copy.width) // 2
            paste_y = (height - img_copy.height) // 2
            background.paste(img_copy, (paste_x, paste_y), img_copy)
            img = background

    # Step C: Filters
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

    if 'blur' in params:
        blur_radius = min(params.get('blur', 0), 50)
        if blur_radius > 0:
            img = img.filter(ImageFilter.GaussianBlur(radius=blur_radius))

    # 3. Save final image to buffer
    buffer = io.BytesIO()
    final_format = 'PNG' if 'A' in img.getbands() else original_format
    img.save(buffer, format=final_format)
    buffer.seek(0)

    mime_type = Image.MIME.get(final_format.upper(), 'image/png')
    
    return buffer.getvalue(), mime_type