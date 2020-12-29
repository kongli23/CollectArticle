import re
import random
import requests
from wp_spider.extractor import Extractor



def down(url):
    resp = requests.get(url)

    ex = Extractor()
    ex.extract(url, resp.text)
    print('标题：{}'.format(ex.title))
    print('正文：{}'.format(ex.format_text))
    content = ex.format_text
    pat = '(<img[\s\S].*?>)'
    pat_list = re.compile(pat,re.IGNORECASE).findall(content)
    # print(pat_list)
    # content = re.sub(pat,'<img src="{}" />'.format(random_imgs()),content)
    # print(content)

    imgs_list = []
    for img in pat_list:
        imgs_list.append(random_imgs())

    rand_img = [str(i) for i in imgs_list]
    html = re.sub(pat,lambda m: '<img src="{}" />'.format(rand_img.pop()), content)
    print('替换：{}'.format(html))

def random_imgs():
    '''
    获取随机生成图片的网址
    :return:
    '''
    img_list = [
        'https://img.catct.cn',
        'https://img.catct.cn/mc.php',
        'https://api.lyiqk.cn/miku',
        'https://api.lyiqk.cn/acg',
        'https://api.ixiaowai.cn/mcapi/mcapi.php'
    ]

    # 随机获取一个图片网址 用于获取随机图片
    current_img = random.choice(img_list)
    resp = requests.get(current_img)
    print('当前：{}'.format(resp.url))
    #https://tva4.sinaimg.cn/large/.jpg
    return resp.url

if __name__ == '__main__':
    down('https://www.gzkd888.com/6207.html')
    # random_imgs()