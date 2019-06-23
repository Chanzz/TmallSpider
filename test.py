from bs4 import BeautifulSoup as bs
import os
import json

BASE_DIR = 'Resources/'
with open('Resources/list.html', 'r', encoding='utf8')as f:
    html = f.read()
bs_html = bs(html, 'html5lib')
# shop_name = bs_html.select('.shop-name > a')
# 获取店铺名称
shop_name = bs_html.find('span', attrs={'class': 'shop-name'}).find('a').get_text().replace(' ', '')[1:-5]
if not os.path.exists(BASE_DIR + 'pic/' + shop_name):
    os.mkdir(BASE_DIR + 'pic/' + shop_name)
# 获取宝贝链接
goods_urls = {}
item3line1_urls = bs_html.find_all('div', attrs={'class': 'item3line1'})
# print(item3line1_urls)
# .find_all('dd',attrs={'class':'detail'})
for item3line1_url in item3line1_urls:
    detail_url = item3line1_url.find_all('a', attrs={'class': 'item-name'})
    for i in detail_url:
        # 商品名称
        goods_name = i.get_text().replace(' ', '')[1:]
        # 商品地址
        # if not i.attrs['hrea']:
        #     print(1)

        goods_url = i.attrs['href']
        goods_urls[goods_name] = goods_url
# 写入文件
# with open(BASE_DIR + 'json/goods_url.json', 'w', encoding='utf-8')as f:
#     json.dump(goods_urls, f, ensure_ascii=False)
print(goods_urls)