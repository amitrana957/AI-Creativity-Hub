from flask import Blueprint, request, jsonify
from services.image_service import generate_image_model
image_bp = Blueprint('image_bp', __name__)
@image_bp.route('/generate', methods=['POST'])
def generate_image():
    try:
        data = request.get_json()
        prompt = data.get('prompt','')
        url = generate_image_model(prompt)
        return jsonify({'image_url': url})
    except Exception as e:
        return jsonify({'error': str(e)}),500

