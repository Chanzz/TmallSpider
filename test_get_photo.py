from selenium import webdriver
from bs4 import BeautifulSoup as bs
from time import sleep
login_url = 'https://login.taobao.com/member/login.jhtml'
import re
browser = webdriver.Chrome()
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
browser = webdriver.Chrome(options=options)
browser.get(login_url)
# 扫码登录时间
sleep(15)
browser.get('https:'+'//item.taobao.com/item.htm?id=592706955113')
html=browser.page_source
bs_html=bs(html,'html5lib')
content=bs_html.find_all('img',attrs={'align':'absmiddle'})
print(content)
# photo=[]
# for i in content:
#     # print(i)
#     photo_url=i.attrs['src']
#     result = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', photo_url)[0]
#     if result=='.jpg':
#         photo.append(photo_url)
#     else:
#         photo.append(i.attrs['data-ks-lazyload'])
# print(photo)




