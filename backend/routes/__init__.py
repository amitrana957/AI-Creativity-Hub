# routes/__init__.py

from flask import Flask
from .text import text_bp
from .image import image_bp
from .audio import audio_bp
from .multimodal import multimodal_bp

# Base prefix for all AI endpoints
AI_PREFIX = "/ai"


def register_blueprints(app: Flask):
    """
    Register all blueprints using the AI_PREFIX constant.
    Change AI_PREFIX here to update all endpoints at once.
    """
    app.register_blueprint(text_bp, url_prefix=f"{AI_PREFIX}/text")
    app.register_blueprint(image_bp, url_prefix=f"{AI_PREFIX}/image")
    app.register_blueprint(audio_bp, url_prefix=f"{AI_PREFIX}/audio")
    app.register_blueprint(multimodal_bp, url_prefix=f"{AI_PREFIX}/multimodal")
