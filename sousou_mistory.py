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
reload(sys)
sys.setdefaultencoding("utf-8")

#Python版本>=3.4
#import importlib
#importlib.reload(sys)

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
		url = 'https://s.taobao.com/search?q=%E6%95%85%E4%BA%8B%E6%9C%BA&imgfile=&js=1&stats_click=search_radio_all%3A1&initiative_id=staobaoz_20190820&ie=utf8'
		headers = {
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
			"cache-control": "max-age=0",
			"cookie": "cna=7JKiEpFHzlMCAd3iIOrTYAwh; t=1e17a93117f164103cc2ac78ef3512b2; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; enc=%2B%2FPNvT4UOUk0ZH95RVO%2BhpnLGpENKcWFl36bVhKrsEPMiqVv%2Ff5JT0WS4sZoOwv9h9GufpldD7eX3oVR9e10cw%3D%3D; miid=7882758021902184618; hng=CN%7Czh-CN%7CCNY%7C156; tracknick=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; thw=cn; _uab_collina=156496885215409652475149; UM_distinctid=16c8876887272e-01f2bccbbcc11c-4f4c0a2e-1fa400-16c887688738fe; _cc_=U%2BGCWk%2F7og%3D%3D; v=0; cookie2=1eb4b2ba76a3586a7b81120e0c33232a; _tb_token_=6b613b73b178; unb=899977127; uc3=id2=W8CE0v8U2F%2FX&nk2=oHTbP%2Flo5ZE%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D&vt3=F8dByua36w8%2FcYInHKI%3D; csg=539d85e9; lgc=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; cookie17=W8CE0v8U2F%2FX; dnk=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; skt=6320dcd93e7a5a49; existShop=MTU3MjQxMzY4Mg%3D%3D; uc4=id4=0%40WeNe2ZWhRAYPgRibTfzu8sGHvZA%3D&nk4=0%40oib6nB2SPAJoGEa33H5vhPy62g%3D%3D; _l_g_=Ug%3D%3D; sg=%E5%A7%AC71; _nk_=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; cookie1=U%2BGWngd%2FhfSbx9oeCKJj37j1xapM4es%2BPmPCtgIAF3k%3D; mt=ci=62_1; uc1=cookie16=U%2BGCWk%2F74Mx5tgzv3dWpnhjPaQ%3D%3D&cookie21=W5iHLLyFfXVRDP8mxoRA8A%3D%3D&cookie15=Vq8l%2BKCLz3%2F65A%3D%3D&existShop=false&pas=0&cookie14=UoTbnxzN%2Brlm4Q%3D%3D&tag=8&lng=zh_CN; x5sec=7b227365617263686170703b32223a223535343562336333306635363735356466653735396364366530663631373239434d5445354f3046454c6178303971486b36504674674561444467354f546b334e7a45794e7a737a4d513d3d227d; JSESSIONID=26E356670896716174E03E9F2BDA8EBA; isg=BLW1YM-VBM2B42BwofdhGAvmxDGvmmq2FQloZjfacSx7DtUA_4J5FMOMXJKdVYH8; l=dBPNlkLlq3EQXURoBOCanurza77OSIRYYuPzaNbMi_5wV6T6lQ_OkN6MWF96VjW5G6YB4Rb-zx99-etkZZVNVi--g3fzgbO3nkY94",
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
