import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

"""
페이지당 20개씩 나옴
"""

def get_page_articles(page):
    # queryTime은 시간이 지나면 바꿔줄 필요가 있음
    url = f"https://kin.naver.com/qna/list.nhn?dirId=208&queryTime=2019-10-21%2015%3A26%3A30&page={page}"
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    refs = soup.select('a')
    refs = [x.get("href") for x in refs]
    refs = filter(lambda x: x.startswith("/qna/detail.nhn"), refs)
    refs = map(lambda x: "https://kin.naver.com" + x, refs)
    refs = set(refs)
    return refs

def get_article_question(url):
    soup = BeautifulSoup(requests.get(url).text, "html.parser")
    title = soup.select_one('div.title')
    title = title.text.strip() if title else ""

    content = soup.select_one('#content > div.question-content > div > div.c-heading._questionContentsArea.c-heading--default-old > div.c-heading__content')
    content = content.text.strip() if content else ""

    return title, content


MAX_PAGES = 100
REQUEST_DELAY = 0

results = []


for page in range(1, MAX_PAGES):
    articles = get_page_articles(page)
    print(f"page #{page} {len(articles)} articles.")
    
    for art in articles:
        title, content = get_article_question(art)
        item = (art, title, content)
        results.append(item)
        print(item)
        time.sleep(REQUEST_DELAY)


pd.DataFrame(results).to_csv("./data/zisikin.csv", index=False, header=False)