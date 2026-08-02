from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# TDnetの最新IRを取得する関数
def crawl_tdnet():
    url = "https://www.release.tdnet.info/inbs/I_main_00.html"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")

    rows = soup.select("table tr")
    ir_list = []

    for row in rows[1:20]:  # 最新20件だけ取得
        cols = row.find_all("td")
        if len(cols) < 5:
            continue
        ir_list.append({
            "date": cols[0].text.strip(),
            "code": cols[1].text.strip(),
            "company": cols[2].text.strip(),
            "title": cols[3].text.strip(),
            "url": "https://www.release.tdnet.info/inbs/" + cols[3].find("a")["href"]
        })

    return ir_list

@app.route("/ir/latest")
def latest_ir():
    tdnet_data = crawl_tdnet()
    return jsonify(tdnet_data)

@app.route("/")
def home():
    return "IR server is running"

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

