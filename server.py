from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

IR_URLS = {
    "7203": {
        "name": "トヨタ自動車",
        "ir_url": "https://global.toyota/en/ir/"
    },
    "6758": {
        "name": "ソニーグループ",
        "ir_url": "https://www.sony.com/en/SonyInfo/IR/"
    },
    # ここに増やしていける
}

def fetch_latest_ir(ir_url):
    try:
        res = requests.get(ir_url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        link = soup.select_one("a[href$='.pdf'], a[href*='pdf'], a[href*='news'], a[href*='release']")
        if link:
            return {
                "title": link.text.strip(),
                "url": link.get("href")
            }
    except:
        pass
    return None

@app.route("/ir/latest")
def latest_ir():
    results = []

    for code, info in IR_URLS.items():
        ir_info = fetch_latest_ir(info["ir_url"])
        if ir_info:
            results.append({
                "code": code,
                "name": info["name"],
                "title": ir_info["title"],
                "url": ir_info["url"]
            })

    if not results:
        return jsonify({"error": "IR情報が取得できませんでした"})

    return jsonify(results)

@app.route("/")
def home():
    return "Nikkei225 IR server is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
