# -*- coding:utf-8 -*-
# Create @ 2019-06-21 16:51:51
# Author @ 819070918@qq.com

import re
import sys
import csv
import json
import time
import requests
from xlwt import Workbook
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

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
	
def write_file(content):
    f = open("text.txt",'wb')
    f.write(content) 

def main(word):
	data = [["名称", "价格", "销量", "链接"]]
	for i in range(page_num):
		url = 'https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20191029&stats_click=search_radio_all%3A1&js=1&imgfile=&q=36%E8%AE%B0%E6%99%BA%E8%83%BD%E6%89%8B%E5%86%99%E6%9C%AC&suggest=0_1&_input_charset=utf-8&wq=36%E8%AE%B0&suggest_query=36%E8%AE%B0&source=suggest'
		headers = {
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
			"cache-control": "max-age=0",
			"cookie": "cna=7JKiEpFHzlMCAd3iIOrTYAwh; t=1e17a93117f164103cc2ac78ef3512b2; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; enc=%2B%2FPNvT4UOUk0ZH95RVO%2BhpnLGpENKcWFl36bVhKrsEPMiqVv%2Ff5JT0WS4sZoOwv9h9GufpldD7eX3oVR9e10cw%3D%3D; miid=7882758021902184618; hng=CN%7Czh-CN%7CCNY%7C156; tracknick=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; thw=cn; _uab_collina=156496885215409652475149; UM_distinctid=16c8876887272e-01f2bccbbcc11c-4f4c0a2e-1fa400-16c887688738fe; _cc_=U%2BGCWk%2F7og%3D%3D; v=0; cookie2=1b553df0625a1c56e14892a01aea4610; _tb_token_=731773ee518a3; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=56F7649EE88344FF8E200BF79B4FC55B; l=dBj4yQHIqRENASKCBOCwSuI8Y0bOSIRAguPRwh4yi_5a-6L1GWQOkaVc1Fp6VjWfThYB4Rb-zx99-etkZLy06Pt-g3fPaxDc.; isg=BJqaMBjUkyI0ux910mpUuO3j60B8Yx15tqC3t6QTRi34FzpRjFtutWBl46Mux5Y9",
			"referer": "https://www.taobao.com/",
			"upgrade-insecure-requests": "1",
			"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36",
		}
		resp = requests.get(url, headers=headers)
		html = resp.text
		content = re.findall(r'g_page_config = (.*?) g_srp_loadCss', html, re.S)[0].strip()[:-1]	
		content = json.loads(content)
		data_list = content['mods']['itemlist']['data']['auctions']
		for item in data_list:
			title = parse_title(item['title'])
			price = item['view_price']
			count = parse_count(item['view_sales'])
			url = item['detail_url']

			data.append([title, price, count, url])

	work_book = Workbook(encoding="utf-8")
	sheet = work_book.add_sheet(word)

	for k, v in enumerate(data):
		for i, j in enumerate(v):
			sheet.write(k, i, label=j)

	current = time.strftime("%Y-%m-%d", time.localtime(time.time()))
	work_book.save('{}_{}.xls'.format(word, current))

	# with open("{}.csv".format(word), 'wb') as fr:
	# 	fw = csv.writer(fr)
	# 	fw.writerows(data)


if __name__ == '__main__':
	word = sys.argv[1]
	main(word)