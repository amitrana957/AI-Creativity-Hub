from flask import Flask
from routes import register_blueprints
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

# Register all blueprints
register_blueprints(app)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
