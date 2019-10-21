import requests
import time
import json
import pandas as pd
from bs4 import BeautifulSoup

REQUEST_DELAY = 0


def get_daily_best_list(page):
    url = f"http://www.ilbe.com/list/ilbe?page={page}&listStyle=list"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    items = soup.select('#content-wrap > div.board-wrap > div.board-list > ul > li')
    
    def is_article(item):
        count = item.select('span.count')[0].text
        return count not in ('공지', '번호', 'AD')
    
    def parse_item(item):
        title = item.select('span.title > a')[0]
        id = title.get('href')
        id = id.split("?")[0].split("/")[-1]
        id = int(id)

        title = title.text

        comment_count = item.select('span.title > span > span > a')[0].text
        comment_count = int(comment_count)

        return (title, id, comment_count)


    items = [parse_item(x) for x in items if is_article(x) ]

    return items

    

def get_article_url(id):
    url = f"http://www.ilbe.com/view/{id}"
    return url

def get_comments(id, page):
    url = f"http://www.ilbe.com/commentlist/{id}?page={page}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    comments = soup.select('span.cmt')
    comments = [x.text for x in comments]
    return comments


articles = []
comments = []


for i in range(1, 3):
    print(f"Start parsing page {i}")

    items = get_daily_best_list(i)
    articles.extend(items)

    time.sleep(REQUEST_DELAY)    

    for item in items:
        (title, id, comment_count) = item

        for j in range(int(comment_count / 100 + 1)):
            c = get_comments(id, j + 1)

            comments.extend([(id, x) for x in c])
            time.sleep(REQUEST_DELAY)



pd.DataFrame(articles).to_csv("./data/ilbe_titles.csv", index=False, header=False)
pd.DataFrame(comments).to_csv("./data/ilbe_comments.csv", index=False, header=False)