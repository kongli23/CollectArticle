import requests
import cchardet
from pybloom_live import BloomFilter
from threading import Thread
from queue import Queue

bloom = BloomFilter(capacity=1e7,error_rate=0.001) #url 去重过滤器

class Get_Code:
    '''
    模拟百度蜘蛛下载类
    '''
    def get_Html(url):
        headers = {
            'user-agent': 'Mozilla/5.0 (compatible; Baiduspider-render/2.0; +http://www.baidu.com/search/spider.html)'
        }
        try:
            resp = requests.get(url, headers, timeout=15)
            html = None
        except requests.RequestException as err:
            print('下载异常：{}'.format(err))
        else:
            text = resp.content  # 这里返回的是二进制的内容
            # 自动识别网页编码
            encoding = cchardet.detect(text)['encoding']
            if encoding is None:
                encoding = 'utf-8'
            html = text.decode(encoding=encoding, errors='ignore')
        return html

class run_start(Thread,Get_Code):
    def __init__(self,get_url_queue):
        super(run_start, self).__init__()
        self.get_url_queue = get_url_queue


    def run(self):
        while True:
            try:
                url = self.get_url_queue.get()   #从关键词列队中提取一个

                # 判断采集过滤器中是否已采集，如果有则跳过，没有则添加
                if url in bloom:
                    continue
                # 过滤器中如果没有当前url则添加，并且写入文件中防止重复采集
                bloom.add(url)
                with open('links.txt','a',encoding='utf-8') as f:
                    f.write(f'\n{url}')

                # # 开始下载源码
                print('正在下载：{}'.format(url))
                # source = self.get_Html(url)
                # if source is None:
                #     continue
                #
                # # 开始提取源码中的内容
                # self.parse_html(source)

            finally:
                self.get_url_queue.task_done()  #无论怎样都要把消息队列处理完
        print(f'过滤器总数：{bloom.count}')

if __name__ == '__main__':
    get_url_queue = Queue()     #url队列

    links = []
    for i in open('links.txt','r',encoding='utf-8'):
        bloom.add(i.strip())
    '''
    http://www.5minutes.com.cn/joanlqhb.html
    http://www.piaowusong.com/ebook1110/78845m/
    http://www.vitop.com/wodxcgetjl/10090.aspx
    '''
    get_url_queue.put('http://www.5minutes.com.cn/joanlqhb.html')
    get_url_queue.put('http://www.piaowusong.com/ebook1110/78845m/')
    get_url_queue.put('http://www.vitop.com/wodxcgetjl/10090.aspx')

    for i in range(5):
        r = run_start(get_url_queue)
        r.setDaemon(True)
        r.start()

    get_url_queue.join()
    print('任务结束')