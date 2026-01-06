from flask import Flask, request, jsonify
import os
from flask_cors import CORS

app = Flask(__name__)

# Datei mit allen gültigen Keys
KEY_FILE = "keys.txt"


@app.route("/check", methods=["POST"])
def check_key():
    data = request.get_json()
    key = data.get("key")

    # Kein Key gesendet
    if not key:
        return jsonify({"success": False, "msg": "Kein Key eingegeben"}), 400

    # Key-Datei existiert nicht
    if not os.path.exists(KEY_FILE):
        return jsonify({"success": False, "msg": "Key-Datei fehlt"}), 500

    # Keys laden
    with open(KEY_FILE, "r") as f:
        keys = [k.strip() for k in f.readlines() if k.strip()]

    # Key nicht vorhanden oder schon benutzt
    if key not in keys:
        return jsonify({"success": False, "msg": "Key ungültig oder bereits benutzt"}), 403

    # 🔥 Key entfernen (Einmal-Key!)
    keys.remove(key)
    with open(KEY_FILE, "w") as f:
        f.write("\n".join(keys))

    return jsonify({"success": True})


@app.route("/")
def home():
    return "SafeExam Server läuft"


if __name__ == "__main__":
    # Für lokal UND Render geeignet
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

