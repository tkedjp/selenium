from time import sleep

from selenium.webdriver.common.by import By

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService

#Seleniumで使用するドライババージョンアップ自動化
from webdriver_manager.chrome import ChromeDriverManager

#保存先
downloadsFilePath = '/Users/'

# Selenium初期化
def initialize():
   new_driver = ChromeDriverManager().install()
   service  = ChromeService(executable_path=new_driver)
   
   options = webdriver.ChromeOptions()
   options.add_argument('--headless')
   prefs = {
       "download.default_directory": downloadsFilePath,
   }
   options.add_experimental_option("prefs", prefs)

   return webdriver.Chrome(service=service, options=options)

URL = 'https://03plus.net/manage/login.php'

driver = initialize()

# ブラウザでurlを開く
driver.get(URL)

#IDの入力
account_id = driver.find_element(By.ID, 'login_id')
account_id.send_keys('xxxxx')
sleep(3)

#IDの入力
account_pw = driver.find_element(By.ID, 'login_passwd')
account_pw.send_keys('xxxxx')
sleep(3)

#ログイン
login = driver.find_element(By.ID, 'login_button')
login.click()
sleep(5)

#請求明細クリック
driver.get('https://03plus.net/manage/payment.php')
sleep(5)

#明細ダウンロードクリック
driver.find_element(By.LINK_TEXT, "ダウンロード").click()
sleep(10)

#ログアウトクリック
driver.find_element(By.LINK_TEXT, "ログアウト").click()
sleep(5)

#確認ボタン押下
from selenium.webdriver.common.alert import Alert
Alert(driver).accept()
sleep(5)

driver.quit()