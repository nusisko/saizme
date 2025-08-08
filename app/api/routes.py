from flask import Blueprint, request, jsonify, send_file
from app.services import transform_service
import io

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        # --- CHANGED: Call the appropriate function from image_service ---
        image_id = transform_service.save_original_image(file)
        return jsonify({
            "success": True,
            "image_id": image_id,
            "message": "Image uploaded successfully."
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route('/view/<image_id>', methods=['GET'])
def view_image(image_id):
    # Dynamically build params dict and handle type conversion
    params = {}
    integer_keys = ['w', 'h', 'blur', 'perfect_fit']
    for key, value in request.args.items():
        if key in integer_keys:
            try:
                params[key] = int(value)
            except (ValueError, TypeError):
                pass
        else:
            params[key] = value

    try:
        image_data, mime_type = transform_service.process_image_on_the_fly(image_id, params)

        # Serve the image directly from memory using send_file
        return send_file(
            io.BytesIO(image_data),
            mimetype=mime_type,
            as_attachment=False
        )
    except FileNotFoundError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500