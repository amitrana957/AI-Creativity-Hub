from flask import Blueprint, request, jsonify
from services.multimodal_service import process_multimodal_model
multimodal_bp = Blueprint('multimodal_bp', __name__)
@multimodal_bp.route('/process', methods=['POST'])
def process():
    try:
        data = request.get_json()
        result = process_multimodal_model(data)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}),500

