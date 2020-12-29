import hashlib
import requests
import time
import random
import re
from wp_spider.translate.user_agent import RandomUserAgent

class translate_youdao():
    def __init__(self, msg):
        self.msg = msg
        self.url = "http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule"
        self.get_ts = self.get_ts()
        self.user_agent = RandomUserAgent

    def get_ts(self):
        # 获取当前时间戳
        s = int(time.time() * 1000)
        return str(s)

    def get_salt(self):
        # salt参数 由时间戳 + 一位随机数组成
        s = str(int(time.time() * 1000)) + str(random.randint(0, 9))
        return s

    def get_sign(self):
        e = self.msg
        i = self.get_salt()
        words = "fanyideskweb" + e + i + "mmbP%A-r6U3Nw(n]BjuEU"
        # MD5加密
        m = hashlib.md5()
        m.update(words.encode("utf-8"))
        return m.hexdigest()

    def get_bv(self):
        n = hashlib.md5()
        n.update(self.user_agent.encode("utf-8"))
        return n.hexdigest()

    def fanyi(self):
        form_data = {
            "i": self.msg,
            "from": "AUTO",
            "to": "AUTO",
            "smartresult": "dict",
            "client": "fanyideskweb",
            "salt": self.get_salt(),
            "sign": self.get_sign(),
            "ts": self.get_ts,
            "bv": self.get_bv(),
            "doctype": "json",
            "version": "2.1",
            "keyfrom": "fanyi.web",
            "action": "FY_BY_REALTlME"
        }
        headers = {
            "Referer": "http://fanyi.youdao.com/",
            "User-Agent": self.user_agent
        }
        res = requests.get("http://fanyi.youdao.com/", headers=headers)
        cookies = res.cookies
        dict = requests.utils.dict_from_cookiejar(cookies)
        if "OUTFOX_SEARCH_USER_ID" in dict:
            headers = {
                # "OUTFOX_SEARCH_USER_ID": dict["OUTFOX_SEARCH_USER_ID"],
                "OUTFOX_SEARCH_USER_ID": dict["OUTFOX_SEARCH_USER_ID"],
                "Referer": "http://fanyi.youdao.com/",
                "User-Agent": self.user_agent
            }
            res = requests.post(self.url, headers=headers, data=form_data)
            return res.content.decode().strip()
        else:
            return "返回出错"

def youdao(words):
    '''
    有道翻译
    :param words:
    :return:
    '''
    youdao = translate_youdao(words)
    result = youdao.fanyi()
    tgt = re.compile(r'"tgt":"(.*?)"').findall(str(result))
    res = str(tgt).replace("'',",'\n\n').replace("', '",'').replace(",', ",'')\
        .replace("', ",'').replace("'",'').replace(r'\\u201D','').replace(r'\\u201C','').replace('[','').replace(']','')\
        .replace(r"\\\\ s",'').replace('< p >','<p>').replace(r"< \\/ p >",'</p>').replace(r"<\\/p>",'</p>')
    return res

def youdao_strat(text):
    '''
    有道翻译，将英文翻译成中文
    :param text: 待翻译的英文
    :return: 返回翻译后的中文
    '''
    res = youdao(text)
    img = 'https://files.jb51.net/image/msb8001.jpg'
    res = res.replace(' # # # # # ','<p align="center"><img src="{}"/></p>'.format(img))
    return res

if __name__ == '__main__':
    with open('tag_en.txt','r',encoding='utf-8') as f:
        text = f.read()
    res = youdao(text)
    img = 'https://files.jb51.net/image/msb8001.jpg'
    res = res.replace(' # # # # # ','<p align="center"><img src="{}"/></p>'.format(img))
    print(res)