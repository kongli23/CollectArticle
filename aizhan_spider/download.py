'''
源码下载类，用来下载源码
'''
import requests

def down_code(url):
    '''
    下载源码内容
    :param url: 待采集的url
    :return: 返回html源码
    '''
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Referer': 'https://www.aizhan.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66'
    }

    try:
        resp = requests.get(url,headers=headers,timeout=15)
        html = None
    except requests.RequestException as err:
        print('下载异常：{}'.format(err))
    else:
        html = resp.text
    return html

def get_html(keywords):
    '''
    关键词转码
    :param keywords:要转码的关键词
    :return: 返回转码后的链接
    '''
    text = '{}'.format(keywords)
    res = text.encode("unicode_escape")
    z = str(res)
    search_key = z.replace(r'\\u','').replace("b'",'').replace("'",'')
    link = 'https://ci.aizhan.com/{}/'.format(search_key)
    htmlcode = down_code(link)
    return htmlcode