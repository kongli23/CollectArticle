'''
自动提取内容类，根据url自动提取文章的标题，正文内容
'''
import os
import requests
import cchardet
import extractor
from threading import Thread
from queue import Queue
from wp_spider.fakeorigin.translate import translate_text

class Down_article(Thread):
    '''
    根据快照解析后的真实地址采集文章
    '''
    headers = {
        'User-Agent':'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)'
    }

    def __init__(self,download_queue):
        super(Down_article, self).__init__()
        self.download_queue = download_queue

    def run(self):
        while True:
            try:
                kw,url = self.download_queue.get()

                # 下载之前依据词创建目录
                path = r'article\\{}'.format(kw)
                if os.path.exists(path):
                    os.makedirs(path)

                # 开始下载文章源码
                source = self.download(kw,url)
                if source is None:
                    continue

                self.extract_content(kw,url,source,path)
            finally:
                self.download_queue.task_done()

    def download(self,kw,url,retrys=3):
        '''
        下载文章源码
        :param kw:
        :return:
        '''

        try:
            resp = requests.get(url, headers=self.headers, timeout=15)
        except requests.RequestException as err:
            html = None
            print('{}:下载文章异常：{}'.format(url, err))

            if retrys > 0:
                return self.download(kw,url,retrys -1)
        else:
            text = resp.content  # 这里返回的是二进制的内容
            encoding = cchardet.detect(text)['encoding']
            if encoding is None:
                encoding = 'utf-8'
            html = text.decode(encoding=encoding, errors='ignore')
        return html

    def extract_content(self,kw,url,source,path):
        '''
        提取文章正文
        :param kw: 关键词
        :param url: 文章的地址
        :param source: 正文代码段
        :return:
        '''
        ex = extractor.Extractor()
        ex.extract(url,source)

        # 过滤文章,质量不少于10000分, 并且字数超过5000的不要(字数太多,翻译容易出错)
        # if ex.score > 10000 and ex.text_count < 5000:
        title = ex.title
        content = ex.format_text    #带源码的内容
        # content = ex.clean_text #不带源码图片，只是纯文字

        # print('标题：{}'.format(title))
        # print('正文：{}'.format(content))
        print('正在伪原创内容中...===============================================')
        res_2 = translate_text(content)
        print('伪原创完毕，等待写入文件')
        # print('伪原创内容：{}'.format(translate_text(content)))
        try:
            with open(path+'{}.html'.format(title),'w',encoding='utf-8') as fw:
                fw.write('原始正文：{}，\n\n=============================伪原创内容：{}'.format(content,res_2))
                print('{}：保存成功'.format(title))
        except os.error as err:
            print('保存内容出错：{}，err：{}'.format(title,err))


if __name__ == '__main__':
    d_queue = Queue()
    d_queue.put(('seo', 'https://zhidao.baidu.com/question/1434508648904305139.html?qbl=relate_question_4&word=seo%BA%CDsem%B5%C4%C7%F8%B1%F0%CA%C7%CA%B2%C3%B4%3F'))
    down = Down_article(d_queue)
    down.start()