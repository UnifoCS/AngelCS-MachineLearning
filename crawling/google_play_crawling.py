from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import os


driver = webdriver.Chrome('./bin/chromedriver')

def get_app_ids():
    url = "https://play.google.com/store/apps/collection/cluster?clp=SiIKGgoUdG9wc2VsbGluZ19mcmVlX0dBTUUQBxgDEgRHQU1F:S:ANO1ljKw1N4&gsr=CiRKIgoaChR0b3BzZWxsaW5nX2ZyZWVfR0FNRRAHGAMSBEdBTUU%3D:S:ANO1ljLsYXQ"
    driver.get(url)
    time.sleep(5)
    
    infinite_down_scroll(driver, 5, 10)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    links = soup.select("div.wXUyZd > a")
    links = [x.get("href") for x in links]
    links = filter(lambda x: x.startswith("/store/apps/details?id="), links)
    ids = map(lambda x: x.split("=")[-1], links)
    ids = set(ids)
    return ids

def get_review_url(app_id):
    url = f"https://play.google.com/store/apps/details?id={app_id}&showAllReviews=true"
    return url

def infinite_down_scroll(driver, pausing_time, max_scrolling=50):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    for i in range(max_scrolling):
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # 혹시 더보기 버튼 뜨면 누름
        try:
            driver.find_element_by_css_selector('div.U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ[jscontroller="VXdfxd"]').click()
        except:
            pass

        # Wait to load page
        time.sleep(pausing_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break

        last_height = new_height
    
    return i

app_ids = [
    # 소녀가극 레뷰 스타라이트 -Re LIVE-
    # 'jp.co.atm.smile.ww',
    # 데일리판타지
    # 'com.guanghuan.czjykr',
    # 프렌즈마블: 3.3.
    'com.kakaogames.frmarble',
    # 세인트세이야: 3.0
    'com.tencent.tmgp.sskkr',
    # 리니지M: 3.2
    'com.ncsoft.lineagem19'
]
app_ids = get_app_ids()
print("인기차트", len(app_ids), app_ids)

result = []

for app_id in app_ids:
    print(f"Get reviews of {app_id}")
    save_file = f"./data/google_play_{app_id}.csv"
    if(os.path.exists(save_file)):
        print("Already crawled... skip!")
        continue
    
    url = get_review_url(app_id)

    driver.get(url)
    time.sleep(5)

    iters = infinite_down_scroll(driver, 5, 20)
    print(f"{iters} iters.")

    soup = BeautifulSoup(driver.page_source, "html.parser")
    comments = soup.select('div.zc7KVe')

    for comment in comments:
        name = comment.select_one('span.X43Kjb').text
        created_date = comment.select_one('span.p2TkOb').text
        text_span = comment.find('span', {'jsname': 'bN97Pc'})
        if not text_span:
            continue
        else:
            text = text_span.text
            
        stars = comment.select('div.pf5lIe > div > div.vQHuPe.bUWb7c')
        rating = len(stars)

        result.append((app_id, name, created_date, text, rating))

    pd.DataFrame(result).to_csv(save_file, index=False, header=False)