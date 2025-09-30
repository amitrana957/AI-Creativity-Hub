# backend/routes.py

from flask import Flask
from text_routes import text_bp
from image_routes import image_bp
from audio_routes import audio_bp
from multimodal_routes import multimodal_bp


def register_routes(app: Flask):
    """
    Register all blueprints with their /ai/... URL prefixes.
    Change the prefix here to update all endpoints at once.
    """
    app.register_blueprint(text_bp, url_prefix="/ai/text")
    app.register_blueprint(image_bp, url_prefix="/ai/image")
    app.register_blueprint(audio_bp, url_prefix="/ai/audio")
    app.register_blueprint(multimodal_bp, url_prefix="/ai/multimodal")
