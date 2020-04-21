# -*- coding:utf-8 -*-
# Create @ 2019-06-21 16:51:51
# Author @ 819070918@qq.com

# 爬取天猫网页商品数据，数据类型为html

import re
import sys
import json
import time
import ast

from xlwt import Workbook
from lxml import etree

# reload(sys)
# sys.setdefaultencoding("utf-8")

# Python版本>=3.4
import importlib

importlib.reload(sys)

size = 60
page_num = 2


def parse_title(title):
    title = title.replace("<span class=H>", "")
    title = title.replace("</span>", "")
    return title


def parse_count(count):
    # coding: utf-8
    c = 10000 if "万" in count else 1
    count = re.findall(r"\d+\.?\d*", count)
    return float(count[0]) * c


def read_file(path):
    # 第三种方法
    f = open(path, "r", encoding="utf-8")
    data = f.readlines()
    f.close()
    return json.dumps(data)


def read_html(path):
    f = open(path, mode='rb+')
    data = f.read().decode('utf-8', 'ignore')
    return data


def write_file(content):
    f = open("text.txt", 'wb')
    f.write(content)


def main(item):
    request_args = {}
    data = [["商品ID", "名称", "价格", "销量", "链接", "店铺"]]
    name = item['name']
    url = item['url']
    cookie = item['cookie']
    for i in range(1, page_num):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "cookie": "",
            "referer": "https://list.tmall.com",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Mobile Safari/537.36",
        }
        # 实现分页
        if i > 0:
            request_args['s'] = size * (i - 1)

        headers['cookie'] = cookie
        try:
            # 请求网页
            # resp = requests.get(url, params=request_args, headers=headers)
            # html = resp.text

            # 取本地.html文件
            html1 = read_html('search_product.html')
            result = etree.HTML(html1)

            # 商品ID
            product_id = result.xpath("//div[contains(@class, 'product')]")
            ids = []
            comp = re.compile('[^0-9^.^ ]')
            for id_item in product_id:
                id = id_item.get('data-id')
                if None == id:
                    continue
                ids.append(comp.sub('', id))

            # 商品名称
            urls = []
            names = []
            product_name = result.xpath(
                "//p[contains(@class, 'productTitle')]/a[contains(@href,'//detail.tmall.com/item.htm?')]")
            for name_item in product_name:
                urls.append(name_item.get('href'))
                title = name_item.get('title')
                names.append(title)

            # 商品价格
            product_price = result.xpath("//p[contains(@class, 'productPrice')]/em/@title")
            prices = []
            for price_item in product_price:
                if None == price_item:
                    continue
                prices.append(comp.sub('', price_item))

            # 商品销量
            product_sales = result.xpath("//p[contains(@class,'productStatus')]/span/em")
            sales = []
            for sales_item in product_sales:
                if None == sales_item:
                    continue
                sales.append(comp.sub('', sales_item.text))

            # 商品店铺
            product_stores = result.xpath(
                "//div[contains(@class,'productShop')]/a[contains(@class,'productShop-name')]")
            stores = []
            print(len(product_stores))
            for store_item in product_stores:
                stores.append(store_item.text)

            for index in range(len(ids)):
                data.append([ids[index], names[index], prices[index], sales[index], urls[index], stores[index]])

        except Exception as e:
            print("(%s)获取数据异常，错误为(%s)" % (name, e))
            pass
            continue

    work_book = Workbook(encoding="utf-8")
    sheet = work_book.add_sheet(name)

    for k, v in enumerate(data):
        for i, j in enumerate(v):
            sheet.write(k, i, label=j)

    current = time.strftime("%Y-%m-%d", time.localtime(time.time()))
    filePath = "./data/" + '{}_{}.xls'.format(name, current)
    work_book.save(filePath)


if __name__ == '__main__':
    try:
        config = read_file('config.txt')
    except Exception as e:
        str = "读取文件异常，错误为(%s)" % (e)
        print(str)
        sys.exit()
    jsonValue = json.loads(config)
    for item in jsonValue:
        itemDict = ast.literal_eval(item)
        main(itemDict)
