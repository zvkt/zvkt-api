from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

API_KEY = "my-super-secret-key"

# Penyimpanan data: name (string), x dan y (integer)
data_points = [
    {"name": "udin", "x": 1, "y": 2},
    {"name": "budi", "x": 3, "y": 4},
]


def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")

        if key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401

        return f(*args, **kwargs)

    return decorated


def is_int(value):
    # bool termasuk subclass int di Python, jadi harus dikecualikan
    return isinstance(value, int) and not isinstance(value, bool)


@app.route("/")
def home():
    return jsonify({"message": "API is running!"})


@app.route("/data", methods=["GET"])
@require_api_key
def get_data():
    return jsonify(data_points)


@app.route("/data", methods=["POST"])
@require_api_key
def create_data():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Body harus berupa JSON"}), 400

    if "name" not in data or "x" not in data or "y" not in data:
        return jsonify({"error": "name, x, dan y wajib diisi"}), 400

    if not isinstance(data["name"], str) or not data["name"].strip():
        return jsonify({"error": "name harus berupa string dan tidak boleh kosong"}), 400

    if not is_int(data["x"]) or not is_int(data["y"]):
        return jsonify({"error": "x dan y harus integer"}), 400

    # Hanya ambil name, x, dan y, field lain dibuang
    point = {"name": data["name"].strip(), "x": data["x"], "y": data["y"]}
    data_points.append(point)

    return jsonify(point), 201


if __name__ == "__main__":
    app.run(debug=True)
