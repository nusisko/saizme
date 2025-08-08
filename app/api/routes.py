from flask import Blueprint, request, jsonify, send_file
from app.services import upload_service, transform_service
import io

api_bp = Blueprint('api', __name__)

@api_bp.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        image_id = upload_service.save_original_image(file)
        return jsonify({
            "success": True,
            "image_id": image_id,
            "message": "Image uploaded successfully."
        }), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_bp.route('/view/<image_id>', methods=['GET'])
def view_image(image_id):
    # Get transformation parameters from the URL query
    params = {
        'w': request.args.get('w', type=int),
        'h': request.args.get('h', type=int),
        'fit': request.args.get('fit', type=str),
        'filter': request.args.get('filter', type=str),
        'blur': request.args.get('blur', type=int)
    }

    try:
        # Generate the transformed image in memory
        image_data, mime_type = transform_service.process_image_on_the_fly(image_id, params)

        if image_data is None:
            return jsonify({"error": "Image not found"}), 404

        # Serve the image directly from memory
        return send_file(
            io.BytesIO(image_data),
            mimetype=mime_type,
            as_attachment=False
        )
    except FileNotFoundError:
        return jsonify({"error": "Image not found"}), 404
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
