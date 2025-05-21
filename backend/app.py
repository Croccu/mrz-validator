import os
import ssl
import redis
from flask import Flask, request, jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS
from pp_validator import validate_mrz as validate_mrz_td3
from id_validator import validate_mrz_td1

app = Flask(__name__, static_folder="build", static_url_path="")

redis_url = os.getenv("REDIS_URL")

if redis_url:
    redis_connection = redis.Redis.from_url(
        redis_url,
        ssl=True,
        ssl_cert_reqs=ssl.CERT_NONE
    )
    storage_uri = redis_url + "?ssl_cert_reqs=none"
else:
    redis_connection = None
    storage_uri = "memory://"

limiter = Limiter(
    app=app,
    key_func=get_remote_address,
    storage_uri=storage_uri,
)

CORS(app, resources={r"/validate": {"origins": ["http://localhost:3000"]}})

@app.route("/api")
def index():
    return "MRZ Validator API is running ✅"

@app.route("/validate", methods=["POST"])
@limiter.limit("6 per minute")
def validate():
    try:
        data = request.get_json()

        mrz1 = data.get("mrz1", "").strip().upper()
        mrz2 = data.get("mrz2", "").strip().upper()
        mrz3 = data.get("mrz3", "")  # optional — don't strip yet

        # Debug print
        print("🚨 ROUTING DEBUG")
        print("MRZ1:", repr(mrz1), "Length:", len(mrz1))
        print("MRZ2:", repr(mrz2), "Length:", len(mrz2))
        print("MRZ3:", repr(mrz3), "Length:", len(mrz3.strip()))

        if len(mrz1) == 30 and len(mrz2) == 30 and len(mrz3.strip()) == 30:
            print("✅ VALIDATING AS ID CARD (TD1)")
            return jsonify(validate_mrz_td1(mrz1, mrz2, mrz3.strip()))
        elif len(mrz1) == 44 and len(mrz2) == 44:
            print("✅ VALIDATING AS PASSPORT (TD3)")
            return jsonify(validate_mrz_td3(mrz1, mrz2))
        else:
            print("❌ INVALID FORMAT")
            return jsonify({"error": "Invalid MRZ format: expected 2×44 (passport) or 3×30 (ID card)."}), 400

    except Exception as e:
        print("❌ EXCEPTION:", str(e))
        return jsonify({"error": f"Validation failed: {str(e)}"}), 400

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_frontend(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, "index.html")

@app.errorhandler(Exception)
def handle_exception(e):
    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
