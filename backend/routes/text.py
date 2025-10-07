from flask import Blueprint, request, jsonify
from services.text_service import ask_text_model
import traceback

text_bp = Blueprint("text_bp", __name__)


@text_bp.route("/ask", methods=["POST"])
def ask_question():
    try:
        data = request.get_json(force=True)
        query = data.get("query")
        session_id = data.get("session_id")

        # --- Input Validation ---
        if not query:
            return jsonify({"error": "'query' parameter is required"}), 400
        if not session_id:
            return jsonify({"error": "'session_id' parameter is required"}), 400

        # --- Run the LCEL chain with session-based memory ---
        answer = ask_text_model(query, session_id)
        return jsonify({"answer": answer})

    except Exception as e:
        # --- Print the error and full traceback to console ---
        print("\n❌ Error in ask_question() route:")
        print(f"Message: {e}")
        print("Traceback:")
        traceback.print_exc()

        # --- Return user-friendly JSON error response ---
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
