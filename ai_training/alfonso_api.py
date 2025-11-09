# alfonso/alfonso_api.py
from flask import Flask, jsonify
import json

app = Flask(__name__)

@app.route("/api/alfonso")
def alfonso_api():
    with open("data/alfonso_tahminleri.json", encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == "__main__":
    app.run(port=5050)
