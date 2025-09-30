from flask import Flask
from routes.text import text_bp
from routes.image import image_bp
from routes.audio import audio_bp
from routes.multimodal import multimodal_bp

app = Flask(__name__)

app.register_blueprint(text_bp, url_prefix="/text")
app.register_blueprint(image_bp, url_prefix="/image")
app.register_blueprint(audio_bp, url_prefix="/audio")
app.register_blueprint(multimodal_bp, url_prefix="/multimodal")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
