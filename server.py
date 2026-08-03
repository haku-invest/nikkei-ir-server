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

    except Exception as e:
        return None

    return None
