from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import jwt
import datetime

app = Flask(__name__)
CORS(app)

# Reemplaza esto con tu App ID y tu clave privada reales de Jitsi (vpaas)
APP_ID = "vpaas-magic-cookie-e5b67798664c4c70a9e180342ebc2285"
PRIVATE_KEY = """-----BEGIN PRIVATE KEY-----
MIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCzL0WC3C56365K
mB5solppF4fWGmem8YL0Uf0SUARVvF5/jBta8n9zLDhhMWqB+KHkS/qvjys3rmgE
7KRMgoNiX9dGkAICOTSdMr/iK3KuNQ8TUPJrR50mR8oi1e3LGqcNlyM48eIs0UGG
QY6jIyN+JyZDOUGbr8zIypQDJvABqm6SPiaB3UmQh9zKbcfXEdXfpJxL2Dv/nRjb
h5R+mf6IK4Rwdn6xd3lglFY1QDJbJBJuMgcU335RDQoIHTaRUecjMw0zKtqVb+x0
J/LguHOnyVWRUQyPyTFnoutD4wfpva6pO/o7RpDbUKuscppbV8UcO9Kiw8HYZwgf
WA9xuLPXAgMBAAECggEBAIncife33k8NgDTGO0pL05Hd19Yj9LHeSWofFr4bMGqi
hnZN3tInl2WOlUY6Vf7vw+c5igO+/HpXxpJbW8G9/MYYhTI2JEV/q/pyjG3ADfj4
u8OZ2RovPDqyq1QIEm/c7sCnEyOB/wmKaoaYM91ScMFj761zBQZ6yO2H5z9RmwE7
yb15OSmGdSHx4LCUfym5Zq03IyHilvuPVrNu/mfkl7hM0KG6xILI0OpfHLOTgH75
87uUZCU7dLleoTK6VGHEKY5eFqZIANlE6NTuyBGjg827u1FWK0OzjO4/gkfiXUX6
CwW5ZlC5MIXH8I2hv+KX2YJ4RDTm/I8Q8iK96tvNE8ECgYEA+ALIpEI2j7ntwgQx
OlCXf+SmCOUDgc5qNMbZClEkyUSBaObGudwQwhV8G/CXVdG7VzRY5DV8ENNuAvM8
t66FTXT0tRGZldt86FHYGLkAc290M6fEN/iR/dyaxOkvOqLmgEyqdHE24e8FQDRx
Js5dTpCnGAORymvLM/MiskUvmWECgYEAuPTp8pmT8ADWf3hfvPLqaix/IUT/ubq6
tKraLtEQ0540sjOZH8AlpR3WcvHjMPnNcjxR8N7kkqKhjufv8xqqDzyr+Q5y9TQD
TYS7gs63ExhikjddEpo3lDNyCLezUExiEZ8hqOlk7PmQTGTzMUC7jDpJ1YJQ4iVl
PUY1Luc2wDcCgYByYFZH6oFfJ1AO+f/59NDpmnk4AOXtJ1SzokDWETX13DISPtvH
O0Y/O8lQ2VPxsBfFz85u8HuXBurlUWffDg1L+3QfTU6XXfHs8lHGlQswMWZVrDlB
1tD9Uo/N3/x3/khvQuwZZ1z4NVMmmQjV7LX7VZq56GuD/tJn0uldbarWAQKBgFVR
5XncDrpwKIK07LUk+a3wyNR4F999nBMrnWprVu/H01dBJinXYYZBtWNg4gT9tyAz
YzlSGO7rxss9gxsJ+dj9i/dgCvfB/qQLztQQt7M/VHlOwMiMC4d6E+ihlT49fh/S
4JwizkPi/AXBq83Upq+RU+4CJ32q8oDJmk8AqekRAoGAQEI/QB+lnf0VqY+tV8Na
MWuwyhYVyB7SKoRk8lwMfo53vGIyJNQByrUFbnuXd7Tm7P4dDZeiC/l+PKRwrUxg
VIGp/nIrTt19+aTkpedHlhgpHyG3x0UbHc3WPlsfJchASzcoEEIS19X/9C9IMsL4
Kvo0/p3OJGCi7McHKonuQbI=
-----END PRIVATE KEY-----"""

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
