# !/usr/bin/python3
# -*- coding:utf-8 -*-
__auther__ = 'gavin'

import requests
import re
import json
import time
from hashlib import md5
import xlwt

# 数据
DATA = []

t = time.localtime()
# 搜索关键字
find_word = 'python'
# 参数
find_arg = {
    'q': find_word,
    'initiative_id': 'staobaoz_%s%02d%02d' % (t[0], t[1], t[2])
}
# 搜索页面url
# https://s.taobao.com/search?q=python&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180305&ie=utf8
first_url = "https://s.taobao.com/search?q=python&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20180305&ie=utf8"

# url = 'https://s.taobao.com/search?q=python&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
# 发送请求
response = requests.get(first_url, params=find_arg)  # response.json()方法同json.loads(response.text)
html = response.text
# 提取，筛选，清洗数据
content = re.findall(r'g_page_config = (.*?)g_srp_loadCss', html, re.S)  # 正则表达式处理的结果是一个列表，取第一个元素（字典）
if not content:
    print('获取数据失败')
    raise RuntimeError

# 格式化，将json格式的字符串切片
content = content[0].strip()[:-1]
# 将json转为dict
content = json.loads(content)

# 借助json在线解析分析，取dict里的具体data
data_list = content['mods']['itemlist']['data']['auctions']

# 提取数据
for item in data_list:
    temp = {
        'title': item['title'],
        'view_price': item['view_price'],
        'view_sales': item['view_sales'],
        'view_fee': '否' if float(item['view_fee']) else '是',
        'isTmall': '是' if item['shopcard']['isTmall'] else '否',
        'area': item['item_loc'],
        'name': item['nick'],
        'detail_url': item['detail_url'],
    }
    DATA.append(temp)

print(len(DATA))  # 36 首页有12条异步加载的数据 ，应该是48

# 保存一下cookie
cookie_ = response.cookies

# 首页有12条异步加载的数据
# url2 = 'https://s.taobao.com/api?_ksTS=1520072935603_226&callback=jsonp227&ajax=true&m=customized&sourceId=tb.index&q=python&spm=a21bo.2017.201856-taobao-item.1&s=36&imgfile=&initiative_id=tbindexz_20170306&bcoffset=0&commend=all&ie=utf8&rn=e061ba6ab95f8c06a23dbe5bfe9a5d94&ssid=s5-e&search_type=item'
ksts = str(int(time.time() * 1000))
url2 = "https://s.taobao.com/api?_ksTS={}_219&callback=jsonp220&ajax=true&m=customized&stats_click=search_radio_all:1&q=java&s=36&imgfile=&bcoffset=0&js=1&ie=utf8&rn={}".format(
    ksts, md5(ksts.encode()).hexdigest())
# 发送请求
response2 = requests.get(url2, params=find_arg, cookies=cookie_)

html2 = response2.text
# print(html2)

data_list = json.loads(re.findall(r'{.*}', html2, re.S)[0])['API.CustomizedApi']['itemlist']['auctions']

# 提取数据
for item in data_list:
    temp = {
        'title': item['title'],
        'view_price': item['view_price'],
        'view_sales': item['view_sales'],
        'view_fee': '否' if float(item['view_fee']) else '是',
        'isTmall': '是' if item['shopcard']['isTmall'] else '否',
        'area': item['item_loc'],
        'name': item['nick'],
        'detail_url': item['detail_url'],
    }
    DATA.append(temp)

print(len(DATA))  # +12 首页有12条异步加载的数据

# 翻页
get_args = {}
cookies = response2.cookies  # 更新一下cookies
for i in range(1, 10):
    ktsts = time.time()
    get_args['_ksTS'] = "%s_%s" % (int(ktsts * 1000), str(ktsts)[-3:])
    get_args['callback'] = "jsonp%s" % (int(str(ktsts)[-3:]) + 1)
    get_args['data-value'] = 44 * i
    get_args['q'] = 'python'

    # url = 'https://s.taobao.com/search?data-key=s&data-value=44&ajax=true&_ksTS=1520091448743_4613&callback=jsonp4614&q=python&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&bcoffset=4&ntoffset=0&p4ppushleft=1%2C48&s=0'
    url = "https://s.taobao.com/search?data-key=s&data-value=44&ajax=true&imgfile=&js=1&stats_click=search_radio_all%3A1&ie=utf8&bcoffset=4&ntoffset=0&p4ppushleft=1%2C48".format(time.time())

    if i > 1:
        get_args['s'] = 44 * (i - 1)
    r3 = requests.get(url, params=get_args, cookies=cookies)
    html = r3.text
    content = re.findall(r'{.*}', html, re.S)[0]
    content = json.loads(content)
    # print(content['mods']['itemlist']['data']['auctions'])
    data_list = content['mods']['itemlist']['data']['auctions']

    # 提取数据
    for item in data_list:
        temp = {
            'title': item['title'],
            'view_price': item['view_price'],
            'view_sales': item['view_sales'],
            'view_fee': '否' if float(item['view_fee']) else '是',
            'isTmall': '是' if item['shopcard']['isTmall'] else '否',
            'area': item['item_loc'],
            'name': item['nick'],
            'detail_url': item['detail_url'],
        }
        DATA.append(temp)

    cookie_ = r3.cookies

    print(len(DATA))  # +12 首页有12条异步加载的数据

    # exit(0) # for test 1 times

# 分析
'''
# 画图
data1 = { '包邮':0, '不包邮':0}
data2 = {'天猫':0, '淘宝':0}
# 地区分布
data3 = {}
for item in DATA:
    if item['view_fee'] == '否':
        data1['不包邮'] += 1
    else:
        data1['包邮'] += 1
    if item['isTmall'] == '是':
        data1['天猫'] += 1
    else:
        data1['淘宝'] += 1
    data3[ item['area'].split(' ')[0] ] = data3.get(item['area'].split(' ')[0], )
print(data1)
draw.pie(data1,'是否包邮')
draw.pie(data2,'是否天猫')
draw.bar(data3,'地区分布')
'''

# 持久化
f = xlwt.Workbook(encoding='utf-8')
sheet01 = f.add_sheet(u'sheet1', cell_overwrite_ok=True)
# 写标题
sheet01.write(0, 0, '标题')
sheet01.write(0, 1, '标价')
sheet01.write(0, 2, '购买人数')
sheet01.write(0, 3, '是否包邮')
sheet01.write(0, 4, '是否天猫')
sheet01.write(0, 5, '地区')
sheet01.write(0, 6, '店名')
sheet01.write(0, 7, 'url')

# write data
for i in range(len(DATA)):
    sheet01.write(i + 1, 0, DATA[i]['title'])
    sheet01.write(i + 1, 1, DATA[i]['view_price'])
    sheet01.write(i + 1, 2, DATA[i]['view_sales'])
    sheet01.write(i + 1, 3, DATA[i]['view_fee'])
    sheet01.write(i + 1, 4, DATA[i]['isTmall'])
    sheet01.write(i + 1, 5, DATA[i]['area'])
    sheet01.write(i + 1, 6, DATA[i]['name'])
    sheet01.write(i + 1, 7, DATA[i]['detail_url'])

f.save(u'搜索%s的结果.xls' % find_word)  # 'python'

