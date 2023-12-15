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
# options.add_argument('--headless')

driver = webdriver.Chrome(
    options=options)

driver.implicitly_wait(10)

driver.get('https://solution.soloel.com/')
sleep(3)

#IDの入力
account_id = driver.find_element(By.ID, 'loginId')
account_id.send_keys(input('IDを入力：'))
sleep(3)

#IDの入力
account_pw = driver.find_element(By.ID, 'password')
account_pw.send_keys(input('パスワードを入力：'))
sleep(3)

#ログイン
login = driver.find_element(By.ID, 'doLogin')
login.click()
sleep(5)

#履歴のページに移動
driver.get('https://solution.soloel.com/buyer/view')
sleep(5)

from_date_input = driver.find_element(By.ID, "serchFromDate")
from_date_input.clear()
from_date_input.send_keys('2020/01/01')
sleep(3)

to_date_input = driver.find_element(By.ID, "serchToDate")
to_date_input.clear()
to_date_input.send_keys('2023/12/31')
sleep(3)

goDoSearch = driver.find_element(By.ID, 'goDoSearch')
goDoSearch.click()

#Pythonファイルのあるディレクトリパス取得
dir_path = os.path.dirname(os.path.abspath(__file__))
html = driver.page_source

#dir_pathの中に，ファイル名{driver.title}.htmlで保存
p = os.path.join(dir_path, 'html', f'{driver.title}.html')
with open(p, 'w') as f:
    f.write(html)

next_page = driver.find_element(By.ID, "goPagerNext")

#htmlの名前にページ番号を振る準備
number = 1

next_page = driver.find_element(By.ID, "goPagerNext")
s = len(str(next_page))
s = int(s)
if s == 0:
    driver.quit()

else:
    #ボタンがあればクリック。なければbreak
    while True:
        try:
            next_page = driver.find_element(By.ID, "goPagerNext")
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