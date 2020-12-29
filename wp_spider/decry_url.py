import requests
from threading import Thread

'''
解析百度快照类
'''
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
            # 此处过滤一些不需要的url，例如百度、搜狐的，360doc文库的
            for con in self.filter_url:
                if con in real_url:
                    return
            self.download_queue.put((kw, real_url))
            with open('autu_getcontent/links.txt', 'a', encoding='utf-8') as f:
                f.write('{}\n'.format(real_url))
            # print((kw, real_url))