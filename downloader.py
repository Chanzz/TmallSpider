import requests
import json
import logging, os, time, random

BASE_DIR = 'Resources/'
PHOTO_DIR = 'Resources/pic/安娜蜜语AnnaSweetT/'
logging.basicConfig(
    filename=os.path.join(os.getcwd(), 'SpiderImgLog.log'),
    format='%(asctime)s  %(filename)s : %(levelname)s  %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %A %H:%M:%S',  # 时间
    level=logging.ERROR,
    filemode='a')


def get_photo(photo_url, name, num):
    # photo_url = 'https://img.alicdn.com/imgextra/i1/826019124/O1CN01m3j2Nl2HGqEkb4FWt_!!826019124.jpg'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36', }
    photo = requests.get(photo_url, headers=headers)
    name=name.replace('/', '')
    with open(PHOTO_DIR + name + str(num) + '.jpg', 'wb')as f:
        f.write(photo.content)
        f.flush()


if __name__ == '__main__':
    with open(BASE_DIR + 'json/img_url.json', 'r', encoding='utf-8')as file:
        urls_dict = json.load(file)
    error_dict = {}
    length = len(urls_dict)
    now = 1
    for k, v in urls_dict.items():
        print('进度{}/{}'.format(now, length))
        print('当前下载页面链接:       ' + k)
        error = []
        now += 1
        for i in range(len(v)):
            try:
                print('第{}张照片'.format(i + 1))
                get_photo(v[i], k, i + 1)
            except Exception as e:
                print('错误原因' + str(e))
                logging.error('错误原因' + str(e))
                error.append(v[i])
        if error:
            error_dict[k] = error
        time.sleep(random.randint(0, 3))
    with open(BASE_DIR + 'json/error_photo_url.json', 'w', encoding='utf-8')as file:
        json.dump(error_dict, file, ensure_ascii=False)
