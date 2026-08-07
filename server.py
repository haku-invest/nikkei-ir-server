import pandas as pd
import requests
from bs4 import BeautifulSoup

def find_ir_url(company_name):
    query = f"{company_name} IR 投資家情報 公式"
    url = f"https://www.bing.com/search?q={query}"

    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        link = soup.select_one("li.b_algo h2 a")
        if link:
            return link.get("href")
    except:
        return None

df = pd.read_csv("nikkei225.csv")  # あなたのCSV
df["ir_url"] = ""

for i, row in df.iterrows():
    name = row["name"]
    print(f"検索中: {name}")
    url = find_ir_url(name)
    df.at[i, "ir_url"] = url if url else ""

df.to_csv("nikkei225_ir_urls.csv", index=False)
print("完成: nikkei225_ir_urls.csv")

