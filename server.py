from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os

app = Flask(__name__)

# 企業のIRページURL（まずはトヨタだけ）
IR_URLS = {
    "7203": {
        "name": "トヨタ自動車",
        "ir_url": "https://global.toyota/en/ir/"
    }
}

# IRページから最新IR情報を取得
def fetch_latest_ir(ir_url):
    try:
        res = requests.get(ir_url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # PDFリンクを広く探索
        link = soup.select_one(
            "a[href$='.pdf'], a[href*='pdf'], a[href*='news'], a[href*='release']"
        )

        if link:
            href = link.get("href")
            absolute_url = urljoin(ir_url, href)  # ← これが絶対URLに変換する
            return {
                "title": link.text.strip(),
                "url": absolute_url
            }

    except Exception as e:
        print("Error:", e)

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
