# -*- coding:utf-8 -*-
import urllib.parse

sss = '一个真正的运营，就等于是一个饭店的经理，决定饭店的装修、菜品、菜价和其它相关的一切，用到网站上就是：运营要决定网站的定位，短中长期的目标，投入，SEO网站排名，并以此搭建团队，建立规则。对网站投入产出结果负责。这是“网站运营”。 而SEO、SEM、设计、客服、文案等等都是按照你的规划来配合你工作的团队岗位之一。 如果一个SEO对网站的投入产出结果负责，那么他就不是SEO，而是一个网站运营。'
text = '{}'.format(sss)
z = urllib.parse.quote(text)
print(z)