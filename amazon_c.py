import os
from time import sleep

from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.common.exceptions import NoSuchElementException

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')

driver = webdriver.Chrome(
    options=options)

driver.implicitly_wait(10)

driver.get('https://www.amazon.co.jp/')
sleep(3)

#検索BOX
search_box = driver.find_element(By.ID, 'twotabsearchtextbox')
search_box.send_keys(input('IDを入力:'))
sleep(3)

search_box.submit()
sleep(3)

#Pythonファイルのあるディレクトリパス取得
dir_path = os.path.dirname(os.path.abspath(__file__))
html = driver.page_source

#dir_pathの中に，ファイル名{driver.title}.htmlで保存
p = os.path.join(dir_path, 'html', f'{driver.title}.html')
with open(p, 'w') as f:
    f.write(html)

# next_page = driver.find_element(By.CLASS_NAME, "s-pagination-item")

#htmlの名前にページ番号を振る準備
number = 1

next_page = driver.find_element(By.LINK_TEXT, "次へ")
s = len(str(next_page))
s = int(s)
if s == 0:
    driver.quit()

else:
    #ボタンがあればクリック。なければbreak
    while True:
        try:
            next_page = driver.find_element(By.LINK_TEXT, "次へ")
            next_page.click()
            sleep(5)

            html = driver.page_source
            number += 1

            p = os.path.join(dir_path, 'html', f'{driver.title+(str(number))}.html')
            with open(p, 'w') as f:
                f.write(html)

        except NoSuchElementException:
            driver.quit()
            break