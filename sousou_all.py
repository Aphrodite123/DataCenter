# -*- coding:utf-8 -*-
# Create @ 2019-06-21 16:51:51
# Author @ 819070918@qq.com

import re
import sys
import csv
import json
import time
import requests
import ast
from xlwt import Workbook
#reload(sys)
#sys.setdefaultencoding("utf-8")

#Python版本>=3.4
import importlib
importlib.reload(sys)

size = 44
page_num = 10

def parse_title(title):
	title = title.replace("<span class=H>", "")
	title = title.replace("</span>", "")
	return title


def parse_count(count):
	# coding: utf-8
	c = 10000 if "万" in count else 1
	count = re.findall(r"\d+\.?\d*", count)
	return float(count[0])*c

def read_file(path):
	# 第三种方法
	f = open(path, "r",encoding='UTF-8')
	data = f.readlines()
	f.close()
	return json.dumps(data)
	
def write_file(content):
    f = open("text.txt",'wb')
    f.write(content) 

def main(item):
	data = [["名称", "价格", "销量", "链接"]]
	name = item['name']
	url = item['url']
	cookie = item['cookie']
	for i in range(page_num):
		headers = {
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "zh-CN,zh;q=0.9",
			"cache-control": "max-age=0",
			"cookie": "",
			"referer": "https://www.taobao.com/",
			"upgrade-insecure-requests": "1",
			"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
		}
		headers['cookie'] = cookie
		try:
			resp = requests.get(url, headers=headers)
			html = resp.text
			content = re.findall(r'g_page_config = (.*?) g_srp_loadCss', html, re.S)
			content = json.loads(content[0].strip()[:-1])
			data_list = content['mods']['itemlist']['data']['auctions']
			for item in data_list:
				title = parse_title(item['title'])
				price = item['view_price']
				count = parse_count(item['view_sales'])
				detailUrl = item['detail_url']

				data.append([title, price, count, detailUrl])
		except Exception as e:
			str = "(%s)获取数据异常，错误为(%s)" %(name,e)
			print(str)
			pass
		continue

	work_book = Workbook(encoding="utf-8")
	sheet = work_book.add_sheet(name)

	for k, v in enumerate(data):
		for i, j in enumerate(v):
			sheet.write(k, i, label=j)

	current = time.strftime("%Y-%m-%d", time.localtime(time.time()))
	filePath = "./data/"+'{}_{}.xls'.format(name, current)
	work_book.save(filePath)

	# with open("{}.csv".format(word), 'wb') as fr:
	# 	fw = csv.writer(fr)
	# 	fw.writerows(data)

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
