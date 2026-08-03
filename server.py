from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup
import os

app = Flask(__name__)

# 企業名から IR ページ URL を取得
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

        # PDFリンクを広く探索
        pdf_links = soup.select("a[href$='.pdf'], a[href*='pdf']")
        if pdf_links:
            link = pdf_links[0]
            return {
                "title": link.text.strip(),
                "url": link.get("href")
            }

        # ニュース系リンクを探索
        news_links = soup.select("a[href*='news'], a[href*='release'], a[href*='ir']")
        if news_links:
            link = news_links[0]
            return {
                "title": link.text.strip(),
                "url": link.get("href")
            }

    except:
        pass

    return None

@app.route("/ir/latest")
def latest_ir():
    company_name = "トヨタ自動車"  # まずは1社だけで動作確認
    ir_url = find_ir_url(company_name)

    if not ir_url:
        return jsonify({"error": "IRページが見つかりませんでした"})

    info = fetch_latest_ir(ir_url)

    if not info:
        return jsonify({"error": "IR情報が取得できませんでした"})

    return jsonify({
        "company": company_name,
        "title": info["title"],
        "url": info["url"]
    })

@app.route("/")
def home():
    return "Nikkei225 IR server is running"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
