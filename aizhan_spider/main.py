import download
import create_excel
from lxml import etree

# PC  https://baidurank.aizhan.com/baidu/www.gifxu.com/
# MB  https://baidurank.aizhan.com/mobile/www.gifxu.com/

# html = download.down_code('https://baidurank.aizhan.com/baidu/www.gifxu.com/')
# print(html)



if __name__ == '__main__':
    # 载入待采集的关键词列表
    for k in open('keys.txt', 'r', encoding='utf-8'):
        html = download.get_html(k.strip())
        etree_html = etree.HTML(html)
        list_keyword = etree_html.xpath('//div[@class="ci-content"]/table/tbody/tr/td[2]/a/@title')   #关键词
        list_index = etree_html.xpath('//div[@class="ci-content"]/table/tbody/tr/td[3]/a/text()')   #PC移动指数
        list_included = etree_html.xpath('//div[@class="ci-content"]/table/tbody/tr/td[5]/text()')   #收录量
        for keyword,index,included in zip(list_keyword,list_index,list_included):
            # print('关键词：{}，指数：{}，收录量：{}'.format(keyword,index,included))
            # 保存已采集的关键词
            create_excel.sava_excel(keyword,index,included)
        print('关键词：{} 采集完毕！'.format(k.strip()))

    print('任务完成！')