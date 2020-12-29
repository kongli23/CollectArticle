'''
伪原创类，将原始中文翻译成英文，再将英文翻译成中文进行文章原创
参数：text 待伪原创的文本
'''
import re
from wp_spider.fakeorigin.tran_google import google_start
from wp_spider.fakeorigin.tran_youdao import youdao_strat

def translate_text(text):
    '''
    传入原始文章，进行中英转换伪原创
    :param text: 伪原创文本
    :return: 返回已伪原创后的文本
    '''
    # 过滤一些特殊的字符
    #[a-z0-9]{9,50}

    rep_str = re.compile(r'[a-z0-9]{15,50}')
    str_text = rep_str.sub('', text)

    # 开始翻译
    en_text = google_start(str_text)
    cn_text = youdao_strat(en_text)
    return cn_text