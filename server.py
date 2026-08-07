from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.route("/ir/latest")
def latest_ir():
    return jsonify({"status": "ok", "message": "server is running"})

@app.route("/")
def home():
    return "Nikkei225 IR server is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
