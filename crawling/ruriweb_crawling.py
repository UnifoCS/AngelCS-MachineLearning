import requests
import time
import json
import pandas as pd
from bs4 import BeautifulSoup

REQUEST_DELAY = 0

BEST_CATEGORIES = [
    'cartoon',
    'political',
    'humor',
    'ghost',
    'community',
    'game',
    'hobby',
    'anime'
]

def get_best_list(category, page, now=False):
    best_type = "now" if now else "hit"
    url = f"https://bbs.ruliweb.com/best/{category}/{best_type}?page={page}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('#best_body > table > tbody > tr')

    def parse(item):
        title = item.select('td.subject a')[0]
        ref = title.get('href')
        title_text = title.text
        
        return title_text, ref

    return [parse(item) for item in items]

def get_comments(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    comments = soup.select('div.comment_view.normal.row tr td.comment > div.text_wrapper > span.text')
    comments = [x.text for x in comments]
    return comments


comments = []

for cat in BEST_CATEGORIES:
    print(f"for category {cat}")

    for best_page in range(1, 3):
        print(f"Parsing page #{best_page}")
        items = get_best_list(cat, best_page)

        for item in items:
            (title, url) = item
            comments.extend([(title, cat, url, c) for c in get_comments(url)])

            time.sleep(REQUEST_DELAY)


pd.DataFrame(comments).to_csv("./data/ruriweb_bests.csv", index=False,header=False)        