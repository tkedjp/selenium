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

    order_tags = soup.select('div.view2_order_history div.view2_record')

    for order_tag in order_tags:
        order_day = order_tag.select_one('div.view2_record_head_box > p > span').text
        # total_price = order_tag.select_one('div.view2_tooltip_status_2 > p').text

        product_tags = order_tag.select('div.view2_record_detail')

        for product_tag in product_tags:
            name_tags = product_tag.select('h3 > a')
            for name_tag in name_tags:
                name = name_tag.text

            price = product_tag.select_one('td.money > span').text

            quantity_tags = product_tag.select('#qtyTd > span')
            for quantity_tag in quantity_tags:
                quantity = quantity_tag.text

            subtotal_tags = product_tag.select('#intaxSubttlAmntTd > span')
            for subtotal_tag in subtotal_tags:
                subtotal = subtotal_tag.text

            list.append({             
                '注文日': order_day,
                # '合計価格': total_price,
                '品名': name,
                '価格': price,
                '数量': quantity,
                '小計(税込)': subtotal,
                })  
            print(list[-1])

df = pd.DataFrame(list)
#重複する行を削除
new_df = df.drop_duplicates()
#注文日の列を降順でソート
df_sorted = new_df.sort_values('注文日', ascending=False)
#csv出力
df_sorted.to_csv('list.csv', index=False, encoding='utf-8-sig')