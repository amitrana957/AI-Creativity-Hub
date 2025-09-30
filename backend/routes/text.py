from flask import Blueprint, request, jsonify
from services.text_service import ask_text_model
text_bp = Blueprint('text_bp', __name__)
@text_bp.route('/ask', methods=['POST'])
def ask_question():
    try:
        data = request.get_json()
        query = data.get('query','')
        answer = ask_text_model(query)
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}),500

