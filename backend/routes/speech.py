from flask import Blueprint, request, jsonify, send_from_directory, url_for
import traceback
import os
from werkzeug.utils import secure_filename
from services.speech_service import generate_story_with_audio, transcribe_audio

speech_bp = Blueprint("speech_bp", __name__)

# Folder where TTS audio files are stored
AUDIO_FOLDER = os.path.join(os.path.dirname(__file__), "../static/audio")
os.makedirs(AUDIO_FOLDER, exist_ok=True)

# Folder to temporarily store uploaded files for transcription
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "../static/tmp")
os.makedirs(UPLOAD_DIR, exist_ok=True)


# ---------------------- TTS: Generate Story ----------------------
@speech_bp.route("/generate-story", methods=["POST"])
def generate_story():
    """
    Endpoint to generate a story from a topic and convert it to audio
    Returns story text and full audio URL.
    """
    try:
        data = request.get_json(force=True)
        topic = data.get("topic")
        session_id = data.get("session_id")

        if not topic:
            return jsonify({"error": "'topic' parameter is required"}), 400
        if not session_id:
            return jsonify({"error": "'session_id' parameter is required"}), 400

        result = generate_story_with_audio(topic, session_id, AUDIO_FOLDER)

        audio_filename = result["audio_file"]
        # Full URL to serve audio
        audio_url = url_for(
            "speech_bp.serve_audio", filename=audio_filename, _external=True
        )

        return (
            jsonify(
                {
                    "story": result["story"],
                    "audio_url": audio_url,
                    "message": "Story generated and audio saved successfully",
                }
            ),
            200,
        )

    except Exception as e:
        print("\n❌ Error in generate_story() route:", e)
        traceback.print_exc()
        return jsonify({"error": "Internal server error", "details": str(e)}), 500


# ---------------------- Serve Audio ----------------------
@speech_bp.route("/audio/<filename>", methods=["GET"])
def serve_audio(filename):
    """
    Serve generated audio files from static/audio folder
    """
    try:
        return send_from_directory(AUDIO_FOLDER, filename)
    except Exception as e:
        print(f"\n❌ Error serving audio file {filename}: {e}")
        traceback.print_exc()
        return jsonify({"error": "Audio file not found", "details": str(e)}), 404


# ---------------------- STT: Transcribe Uploaded Audio ----------------------
@speech_bp.route("/transcribe", methods=["POST"])
def transcribe():
    """
    Endpoint to receive an uploaded audio file and return transcript
    """
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_DIR, filename)
        file.save(file_path)

        # Transcribe using speech_service
        transcript = transcribe_audio(file_path)

        # Remove temporary file
        os.remove(file_path)

        return (
            jsonify({"transcript": transcript, "message": "Transcription successful"}),
            200,
        )

    except Exception as e:
        print(f"\n❌ Error transcribing file {file.filename}: {e}")
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
