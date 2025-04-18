from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import jwt
import datetime
from dotenv import load_dotenv
import os

app = Flask(__name__)
CORS(app)

load_dotenv()

# Reemplaza esto con tu App ID y tu clave privada reales de Jitsi (vpaas)
APP_ID = os.getenv("APP_ID")
PRIVATE_KEY = os.getenv("PRIVATE_KEY").replace('\\n', '\n')

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/token", methods=["POST"])
def generate_token():
    data = request.get_json()
    user = data.get("user", {})
    room = data.get("room", "*")  # "*" para todas las salas

    payload = {
        "aud": "jitsi",
        "iss": "chat",
        "sub": APP_ID,
        "room": room,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
        "nbf": datetime.datetime.utcnow(),
        "context": {
            "user": {
                "name": user.get("name"),
                "email": user.get("email"),
                "avatar": user.get("avatar", ""),
                "id": user.get("id"),
                "moderator": user.get("moderator", True)
            },
            "features": {
                "livestreaming": True,
                "recording": True,
                "transcription": True,
                "outbound-call": True
            }
        }
    }

    headers = {
    "kid": "vpaas-magic-cookie-e5b67798664c4c70a9e180342ebc2285/7c6934"
    }

    token = jwt.encode(payload, PRIVATE_KEY, algorithm="RS256", headers=headers)
    return jsonify({"token": token})


if __name__ == "__main__":
    app.run(debug=True)
