import requests
import time
from threading import Thread
from queue import Queue
from lxml import etree
import urllib.parse

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
            time.sleep(30)

    def download(self, kw, retrys=3):
        '''
        下载源码
        :param kw:
        :return:
        '''
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Referer': 'https://www.baidu.com/s?wd={}&pn=10'.format(urllib.parse.quote(kw)),
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.60'
        }
        query = 'https://www.baidu.com/s?wd={}&rsv_spt=1&rsv_iqid=0xeea364ab000326ec&issp=1&f=8&rsv_bp=1&rsv_idx=2&ie=utf-8&tn=baiduhome_pg&rsv_enter=0&rsv_dl=ib&rsv_sug3=1&rsv_btype=i'
        try:
            resp = requests.get(query, headers=headers, timeout=30)
        except requests.RequestException as err:
            print('{}:获取快照异常：{}'.format(query, err))
            html = None
            print('获取快照太快，休眠2秒继续')
            if retrys > 0:
                time.sleep(30)
                return self.download(kw, retrys - 1)
        else:
            resp.encoding = 'utf-8'
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
            print('获取的快照：{}'.format((kw,str_url)))
            self.link_queue.put((kw,str_url))

class Decry_urllist(Thread):
    '''
    解析得到的快照链接,获取真实文章url地址
    '''
    def __init__(self,link_queue,download_queue,filter_url):
        super(Decry_urllist, self).__init__()
        self.link_queue = link_queue
        self.download_queue = download_queue
        self.filter_url = filter_url

    def run(self):
        while True:
            kw,url = self.link_queue.get()
            self.get_decr_url(kw,url)
            self.link_queue.task_done()

    def get_decr_url(self,kw,url):
        try:
            resp = requests.head(url)
        except requests.RequestException as err:
            print('解析快照链接异常: {}'.format(err))
        else:
            real_url = resp.headers.get('Location')
            for con in self.filter_url:
                if con in real_url:
                    return
            # self.download_queue.put((kw, real_url))
            print('快照：{}'.format((kw, real_url,url)))


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

    # # 加载过滤url
    # filter_url = []
    # for k in open('filter_url.txt', 'r', encoding='utf-8'):
    #     filter_url.append(k.strip())
    #
    # # 解析快照链接类
    # # for i in range(15):
    # d = Decry_urllist(link_queue,download_queue,filter_url)
    # d.setDaemon(True)
    # d.start()


    kw_queue.join()
    link_queue.join()
    download_queue.join()
    print('采集结束！')