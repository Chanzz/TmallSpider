from selenium import webdriver
from time import sleep
import requests
from bs4 import BeautifulSoup as bs
import os
import json
import logging

logging.basicConfig(
    filename=os.path.join(os.getcwd(), 'SpiderLog.txt'),
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
    level=logging.ERROR,
    filemode='a')

# 根据店铺页面，获取所有宝贝链接
login_url = 'https://login.taobao.com/member/login.jhtml'
shop_url = 'https://annamiyu.taobao.com/search.htm?spm=a1z10.1-c-s.w5001-17456993967.3.625d3f4bcYPhxI&search=y&scene=taobao_shop'
BASE_DIR = 'Resources/'


# 获取当前页面所有商品链接
def get_good_url(html, good_urls):
    bs_html = bs(html, 'html5lib')
    # shop_name = bs_html.select('.shop-name > a')
    # 获取店铺名称
    shop_name = bs_html.find('span', attrs={'class': 'shop-name'}).find('a').get_text().replace(' ', '')[1:-5]
    if not os.path.exists(BASE_DIR + 'pic/' + shop_name):
        os.mkdir(BASE_DIR + 'pic/' + shop_name)
    # 获取宝贝链接
    item3line1_urls = bs_html.find_all('div', attrs={'class': 'item3line1'})
    for item3line1_url in item3line1_urls:
        detail_url = item3line1_url.find_all('a', attrs={'class': 'item-name'})
        for i in detail_url:
            # 商品名称
            goods_name = i.get_text().replace(' ', '')[:]
            # 商品地址
            good_url = i.attrs['href']
            good_urls[goods_name] = good_url
    return good_urls


def login():
    browser = webdriver.Chrome()
    options = webdriver.ChromeOptions()
    # options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # 不加载图片,加快访问速度
    options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 此步骤很重要，设置为开发者模式，防止被各大网站识别出来使用了Selenium
    browser = webdriver.Chrome(options=options)
    browser.get(login_url)
    # 扫码登录时间
    sleep(15)
    return browser


def get_all_page():
    goods_urls = {}
    browser = login()
    try:
        for i in range(1, 15):
            print('当前爬取商铺页数：' + str(i))
            current_page_url = shop_url + '&pageNo=' + str(i)
            browser.get(current_page_url)
            list_html = browser.page_source
            get_good_url(list_html, goods_urls)
            sleep(5)
    except:
        print('页数已结束')
        pass
    # 写入文件
    with open(BASE_DIR + 'json/goods_url.json', 'a', encoding='utf-8')as f:
        json.dump(goods_urls, f, ensure_ascii=False)


def get_photo_url(flag):
    img_urls = {}
    # 读取文件,1表示更新
    if flag == 1:
        with open(BASE_DIR + 'json/new_goods_url.json', 'r', encoding='utf-8')as f:
            urls_dict = json.load(f)
    else:
        with open(BASE_DIR + 'json/goods_url.json', 'r', encoding='utf-8')as f:
            urls_dict = json.load(f)
    browser = login()
    for k, v in urls_dict.items():
        # 读取文件
        try:
            with open(BASE_DIR + 'json/img_url.json', 'r', encoding='utf-8')as f:
                img_urls = json.load(f)
        except:
            pass
        print("当前爬取商品名：{}   商品链接：{}".format(k, v))
        try:
            browser.get('https:' + v)
        except Exception as e:
            print('错误原因' + str(e))
            logging.error('错误原因' + str(e))
            logging.error('错误位置' + v)
        html = browser.page_source
        bs_html = bs(html, 'html5lib')
        # 获取图片链接
        photo_urls = bs_html.find_all('img', attrs={'align': 'absmiddle'})
        photo = []
        for i in photo_urls:
            photo_url = i.attrs['src']
            # result = re.findall(r'\.[^.\\/:*?"<>|\r\n]+$', photo_url)[0]
            # if result == '.jpg':
            try:
                photo.append(i.attrs['data-ks-lazyload'])
            except:
                photo.append(photo_url)
                pass
            # except Exception as e:
            #     print('错误原因' + str(e))
            #     logging.error('错误原因' + str(e))
            #     logging.error('错误位置' + v)
            #     pass
        try:
            img_urls[k] = photo
        except Exception as e:
            print('已存在')
            pass
        sleep(5)
        with open(BASE_DIR + 'json/img_url.json', 'w', encoding='utf-8')as f:
            json.dump(img_urls, f, ensure_ascii=False)
        # 把新链接写入主文件，并清空
        if flag == 1:
            with open(BASE_DIR + 'json/goods_url.json', 'rw', encoding='utf-8')as f:
                old_urls_dict = json.load(f)
                old_urls_dict.update(urls_dict)
                json.dump(old_urls_dict, f, ensure_ascii=False)
            with open(BASE_DIR + 'json/new_goods_url.json', 'w', encoding='utf-8')as f:
                f.truncate()


# 查找新商品链接
def get_new_photo_url():
    print('更新链接，写入文件中............')
    with open(BASE_DIR + 'json/goods_url.json', 'r', encoding='utf-8')as f:
        urls_dict = json.load(f)
    goods_urls = {}
    browser = login()
    try:
        # 默认为爬取第一页，太久没爬可以改
        for i in range(1, 2):
            print('当前爬取商铺页数：' + str(i))
            current_page_url = shop_url + '&pageNo=' + str(i)
            browser.get(current_page_url)
            list_html = browser.page_source
            get_good_url(list_html, goods_urls)
            sleep(5)
    except:
        print('页数已结束')
        pass
    # 对比文件
    for k in goods_urls.keys():
        if k in urls_dict.keys():
            goods_urls.pop(k)
    # 写入文件
    with open(BASE_DIR + 'json/new_goods_url.json', 'a', encoding='utf-8')as f:
        json.dump(goods_urls, f, ensure_ascii=False)


if __name__ == '__main__':
    # 爬取新店铺
    # get_all_page()
    # get_photo_url(0)
    print('===================================')
    # 更新店铺
    # get_new_photo_url()
    # get_photo_url(1)
    print('===================================')
