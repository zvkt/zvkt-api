
from flask import Flask, request, jsonify
from functools import wraps

app = Flask(__name__)

API_KEY = "my-super-secret-key"

users = [
    {"id": 1, "name": "Raihan", "age": 18},
    {"id": 2, "name": "Budi", "age": 19}
]

messages = [
    {"time": 1, "name": "Raihan", "message": "Hello!"},
    {"time": 2, "name": "Budi", "message": "Hi!"}
]

def require_api_key(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        key = request.headers.get("X-API-Key")

        if key != API_KEY:
            return jsonify({"error": "Invalid API key"}), 401

        return f(*args, **kwargs)

    return decorated


@app.route("/")
def home():
    return jsonify({"message": "API is running!"})


# USERS

@app.route("/users", methods=["GET"])
@require_api_key
def get_users():
    return jsonify(users)


@app.route("/users", methods=["POST"])
@require_api_key
def create_user():
    data = request.json

    user = {
        "id": len(users) + 1,
        "name": data["name"],
        "age": data["age"]
    }

    users.append(user)

    return jsonify(user), 201


# MESSAGES

@app.route("/message", methods=["GET"])
@require_api_key
def get_messages():
    return jsonify(messages)


@app.route("/message", methods=["POST"])
@require_api_key
def create_message():
    data = request.json

    message = {
        "time": len(messages) + 1,
        "name": data["name"],
        "message": data["message"]
    }

    messages.append(message)

    return jsonify(message), 201


if __name__ == "__main__":
    app.run(debug=True)
