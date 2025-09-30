from flask import Blueprint, request, jsonify
from services.audio_service import transcribe_audio_model
audio_bp = Blueprint('audio_bp', __name__)
@audio_bp.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({'error':'No file uploaded'}),400
        file=request.files['file']
        text = transcribe_audio_model(file)
        return jsonify({'transcription': text})
    except Exception as e:
        return jsonify({'error': str(e)}),500

