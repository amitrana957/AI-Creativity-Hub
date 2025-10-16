# routes/__init__.py

from flask import Flask
from .text import text_bp
from .speech import speech_bp

# Base prefix for all AI endpoints
AI_PREFIX = "/ai"


def register_blueprints(app: Flask):
    """
    Register all blueprints using the AI_PREFIX constant.
    Change AI_PREFIX here to update all endpoints at once.
    """
    app.register_blueprint(text_bp, url_prefix=f"{AI_PREFIX}/text")
    app.register_blueprint(speech_bp, url_prefix=f"{AI_PREFIX}/audio")
