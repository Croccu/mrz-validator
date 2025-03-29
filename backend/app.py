from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from mrz_validator import validate_mrz
import os


app = Flask(__name__, static_folder='../frontend/build', static_url_path='')

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")

limiter = Limiter(
    get_remote_address,
    app=app,
    storage_uri=REDIS_URL,
    default_limits=["15 per minute"]  # Adjust as needed
)

CORS(app, resources={r"/validate": {"origins": ["http://localhost:3000"]}})

@app.route("/validate", methods=["POST"])
@limiter.limit("6 per minute")
def validate():
    try:
        data = request.get_json()
        mrz1 = data.get("mrz1", "")
        mrz2 = data.get("mrz2", "")
        result = validate_mrz(mrz1, mrz2)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Validation failed: {str(e)}"}), 400

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

def handle_exception(e):
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
