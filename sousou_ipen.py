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
		url = 'https://s.taobao.com/search?q=%E7%82%B9%E8%AF%BB%E7%AC%94&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306'
		headers = {
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
			"cache-control": "max-age=0",
			"cookie": "cna=7JKiEpFHzlMCAd3iIOrTYAwh; t=1e17a93117f164103cc2ac78ef3512b2; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; enc=%2B%2FPNvT4UOUk0ZH95RVO%2BhpnLGpENKcWFl36bVhKrsEPMiqVv%2Ff5JT0WS4sZoOwv9h9GufpldD7eX3oVR9e10cw%3D%3D; miid=7882758021902184618; hng=CN%7Czh-CN%7CCNY%7C156; tracknick=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; thw=cn; _uab_collina=156496885215409652475149; UM_distinctid=16c8876887272e-01f2bccbbcc11c-4f4c0a2e-1fa400-16c887688738fe; _cc_=U%2BGCWk%2F7og%3D%3D; v=0; cookie2=11ee392c73a25272d447243cbbecfc86; _tb_token_=3f35efee0513; x5sec=7b227365617263686170703b32223a2236643064653737653133353236323339656466396364306539396139343932384349434e344f3046454e36633366362f7a7075694a426f4c4f446b354f5463334d5449334f7a633d227d; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=0D521DF07FBBFE95EB6D95A28DCE500A; l=dBPNlkLlq3EQXRIoBOCwSuI8Y0bOSIRAguPRwh4yi_5aY6L_ts_OkNQERFp6VjWfTKYB4Rb-zx99-etkiKy06Pt-g3fPaxDc.; isg=BMjIpnnGAVO4dW3XNBREdwYVmTYa2S-nKDolAYJ5FMM2XWjHKoH8C15f0XWI7eRT",
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
