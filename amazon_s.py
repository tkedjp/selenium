import re
import os
from glob import glob

from bs4 import BeautifulSoup
import pandas as pd

#htmlファイルのあるディレクトリパス取得
html_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'html', '*')

list = []

for path in glob(html_path):
    with open(path, 'r') as f:
        html = f.read()

    soup = BeautifulSoup(html, 'lxml')

    good_tags = soup.select('div.puis-card-container')

    for good_tag in good_tags:
        price_tag = good_tag.select_one('span.a-price-whole')
        if price_tag is None:
            price_tag = None
        else:
            price = price_tag.text
        # print(price_tag)
        # if not price_tag == '0':
        #     price = price_tag
            name = good_tag.select_one('span.a-size-base-plus').text

            url_tag = good_tag.select_one('.a-link-normal').get('href')
            url = 'https://www.amazon.co.jp' + url_tag
            if 'dp/' in url:
                asin_code = url[url.find('dp/')+3:url.find('dp/')+13]

            else:
                asin_code = '-'

            list.append({             
                '商品名': name,
                '価格': price,
                'URL': url,
                'ASIN':asin_code
                })  
            print(list[-1])

#csv出力
df = pd.DataFrame(list)
df.to_csv('list.csv', index=False, encoding='utf-8-sig')