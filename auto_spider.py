import requests
import time
from threading import Thread
from queue import Queue
from lxml import etree
import decry_url
import get_article

class GetLinks(Thread):
    '''
    根据关键词获取百度快照链接
    '''

    def __init__(self, kw_queue, link_queue):
        super(GetLinks, self).__init__()
        self.kw_queue = kw_queue
        self.link_queue = link_queue

    def run(self):
        while True:
            try:
                kw = self.kw_queue.get()

                print('正在下载：{}，源码'.format(kw))
                source = self.download(kw)
                if source is None:
                    continue

                self.extract_links(kw, source)
            finally:
                self.kw_queue.task_done()

            # 遍历一次暂停30秒
            time.sleep(60)

    def download(self, kw, retrys=3):
        '''
        下载源码
        :param kw:
        :return:
        '''
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
        }

        query = 'https://www.baidu.com/s?'
        params = {
            'wd':'{}'.format(kw),
            'pn':0,
            'rn':50,
            'ie':'utf-8'
        }
        try:
            resp = requests.get(query, headers=headers,params=params,timeout=30)
        except requests.RequestException as err:
            print('{}:获取快照异常：{}'.format(query, err))
            html = None
            print('获取快照太快，休眠2秒继续')
            if retrys > 0:
                time.sleep(30)
                return self.download(kw, retrys - 1)
        else:
            html = resp.text
        return html

    def extract_links(self,kw,source):
        '''
        提取链接
        :param kw:
        :param source:
        :return:
        '''
        link_etree = etree.HTML(source)
        link_list = link_etree.xpath('//div[@id="content_left"]//h3/a/@href')
        for url in link_list:
            str_url = str(url)  # lxml占用过多内存,转换为字符串并将其存储,这样可以防止整个树被垃圾回收
            str_url = str_url.replace('http://','https://')
            self.link_queue.put((kw,str_url))


# 开始运行
if __name__ == '__main__':
    kw_queue = Queue()
    link_queue = Queue()
    download_queue = Queue()

    # 载入待采集的关键词列表
    for k in open('nvyoudaquan.txt', 'r', encoding='utf-8'):
        kw_queue.put(k.strip())

    # 下载快照链接类
    # for i in range(5):
    s = GetLinks(kw_queue, link_queue)
    s.setDaemon(True)
    s.start()

    # 加载过滤url
    filter_url = []
    for k in open('filter_url.txt', 'r', encoding='utf-8'):
        filter_url.append(k.strip())

    # 解析快照链接类
    # for i in range(15):
    d = decry_url.Decry_urllist(link_queue,download_queue,filter_url)
    d.setDaemon(True)
    d.start()

    # 下载文章处理类
    # for i in range(10):
    d = get_article.Down_article(download_queue)
    d.setDaemon(True)
    d.start()


    kw_queue.join()
    link_queue.join()
    download_queue.join()
    print('采集结束！')