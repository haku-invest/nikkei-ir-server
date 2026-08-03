from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

app = Flask(__name__)

# 企業名から IR ページ URL を自動取得
def find_ir_url(company_name):
    query = f"{company_name} IR 投資家情報"
    url = f"https://www.bing.com/search?q={query}"

    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        link = soup.select_one("li.b_algo h2 a")
        if link:
            return link.get("href")
    except:
        pass

    return None


# IR ページから最新 IR 情報を取得
def fetch_latest_ir(ir_url):
    try:
        res = requests.get(ir_url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # よくある IR ページの構造
        link = soup.select_one("a[href*='pdf'], a[href*='IR'], a[href*='news'], a[href*='release']")
        if link:
            return {
                "title": link.text.strip(),
                "url": link.get("href")
            }
    except:
        pass

    return None


# /ir/latest のメイン処理
@app.route("/ir/latest")
def latest_ir():
    df = pd.read_csv("nikkei225.csv", encoding="utf-8")

    results = []

    for _, row in df.iterrows():
        ir_url = find_ir_url(row["name"])
        if not ir_url:
            continue

        info = fetch_latest_ir(ir_url)
        if info:
            results.append({
                "code": row["code"],
                "name": row["name"],
                "title": info["title"],
                "url": info["url"]
            })

    return jsonify(results)


@app.route("/")
def home():
    return "Nikkei225 IR server is running"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
