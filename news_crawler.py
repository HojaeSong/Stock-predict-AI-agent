'''
====임시 READ ME====
1. Terminal에서 pip install requests, trafilatura 해야함
2. news api key는 본인이 발급받은 고유한 키 써야하므로 다른 파일에 입력하도록 함. (지금은 이채영꺼 입력해둠)
3. 검색어, 추출할 뉴스의 개수는 아직까진 input()으로 받도록 함.
4. 검색어는 2개 이상 입력해야 결과가 유의미할 확률up, (AND 또는 OR 사용하면 됨, 대문자 필수)
'''

import os
import time
import requests
import trafilatura
import apikey

API_KEY = os.getenv("NEWSAPI_KEY", apikey.YOUR_NEWAPI_KEY)
NEWSAPI_URL = "https://newsapi.org/v2/everything"

def fetch_news_urls(query, page_size):
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "pageSize": page_size,
        "apiKey": API_KEY,
    }
    r = requests.get(NEWSAPI_URL, params=params, timeout=12)
    r.raise_for_status()
    data = r.json()
    articles = data.get("articles", [])

    return [(a.get("title"), a.get("url"), a.get("publishedAt")) for a in articles if a.get("url")]


def extract_article_text(url):
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return "text not downloaded"
    text = trafilatura.extract(
        downloaded,
        include_comments=False,
        include_tables=False,
        favor_recall=True,
    )
    return text or ""

if __name__ == "__main__":
    query = input("검색어 입력: ")
    page_size = input("뉴스 몇개 출력 예정?: ")

    results = fetch_news_urls(query, page_size)

    for i, (title, url, published) in enumerate(results, start=1):
        print(f"{i}. ({published[:10]}) {title}")

    print()

    for i, (title, url, published) in enumerate(results, start=1):
        print(f"[{i}] {title}\n{url}\n")
        article_text = extract_article_text(url)
        if article_text:
            print("--- Article Content ---")
            print(article_text[:])
        else:
            print("extract failed")
        print()
        time.sleep(1)
