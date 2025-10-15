from flask import Blueprint, request, jsonify, send_file
import traceback
import os
from services.speech_service import generate_story_with_audio


speech_bp = Blueprint("speech_bp", __name__)


@speech_bp.route("/generate-story", methods=["POST"])
def generate_story():
    """
    Endpoint to generate a story from a topic and convert it to audio

    Expected JSON:
    {
        "topic": "A brave knight and a dragon",
        "session_id": "user123"
    }

    Returns:
    {
        "story": "Once upon a time...",
        "audio_file": "story_user123_timestamp.mp3"
    }
    """
    try:

        data = request.get_json(force=True)
        topic = data.get("topic")
        session_id = data.get("session_id")

        # --- Input Validation ---
        if not topic:
            return jsonify({"error": "'topic' parameter is required"}), 400
        if not session_id:
            return jsonify({"error": "'session_id' parameter is required"}), 400

        # --- Generate story and audio ---
        result = generate_story_with_audio(topic, session_id)

        return (
            jsonify(
                {
                    "story": result["story"],
                    "audio_file": result["audio_file"],
                    "message": "Story generated and audio saved successfully",
                }
            ),
            200,
        )

    except Exception as e:
        # --- Print the error and full traceback to console ---
        print("\n❌ Error in generate_story() route:")
        print(f"Message: {e}")
        print("Traceback:")
        traceback.print_exc()

        # --- Return user-friendly JSON error response ---
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
