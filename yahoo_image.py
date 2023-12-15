from time import sleep
import pandas as pd

from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
# options.add_argument('--headless')

driver = webdriver.Chrome(
    options=options)

driver.implicitly_wait(10)

driver.get('https://search.yahoo.co.jp/image')
sleep(3)

search_box = driver.find_element(By.CLASS_NAME, 'SearchBox__searchInput')
sleep(3)

query =input('キーワードを入力:')
search_box.send_keys(query)
sleep(3)

search_box.submit()
sleep(3)

# 1000ずつスクロールし，3000より少ない数までスクロール
# height = 1000
# while height < 3000:
#     driver.execute_script("window.scrollTo(0,{});".format(height))
#     height += 1000
#     print(height)

#     sleep(1)

#スクロールしていない高さを取得。一番下までスクロールして数を変数heightに代入。変数new_hightを準備
height = driver.execute_script("return document.body.scrollHeight") #初期値が1,000なら
new_height = 0

#while文。スクロールした分さらにスクロール
while True:
    driver.execute_script(f'window.scrollTo(0, {height});') #初期値1,000だけスクロールする
    sleep(5)
    #さらに一番下までスクロールして数を変数new_heightに代入し，もしnew_heightとheightの数が等しくなったらbreak
    new_height = driver.execute_script("return document.body.scrollHeight") #一番下までスクロールするので2,000
    if height == new_height: #new_heightが更新されなかったら，つまりスクロールできなかったらbreak

        #もっと見るボタンのCSSセレクタを取得する
        search_more_button = driver.find_elements(By.CLASS_NAME, 'sw-Button')
        sleep(2)

        #ボタンを押す
        if search_more_button:
            search_more_button[0].click()

        else:
            break

    else:
        break    

    height = new_height #変数heightは2,000になる

#画像の要素を選択する
elements = driver.find_elements(By.CLASS_NAME, 'sw-Thumbnail')

d_list = []
#要素からURLを取得する
for i, element in enumerate(elements, start=1):
    name = f'{query}_{i}' 
    raw_url = element.find_element(By.CLASS_NAME, 'sw-ThumbnailGrid__details').get_attribute('href')
    yahoo_image_url = element.find_element(By.TAG_NAME, 'img').get_attribute('src')
    title = element.find_element(By.TAG_NAME, 'img').get_attribute('alt')

    d = {
        'filename': name,
        'raw_url': raw_url,
        'yahoo_image_url' : yahoo_image_url,
        'title': title,
    }

    d_list.append(d)
    print(d_list[-1])

    sleep(2)

df = pd.DataFrame(d_list)
df.to_csv('image_urls_' + query + '.csv', index=False, encoding='utf-8-sig')    

driver.quit()