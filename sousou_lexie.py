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
		url = 'https://s.taobao.com/search?initiative_id=tbindexz_20170306&ie=utf8&spm=a21bo.2017.201856-taobao-item.2&sourceId=tb.index&search_type=item&ssid=s5-e&commend=all&imgfile=&q=%E4%B9%90%E5%86%99%E6%B6%B2%E6%99%B6%E6%89%8B%E5%86%99%E6%9D%BF&suggest=0_1&_input_charset=utf-8&wq=%E4%B9%90%E5%86%99&suggest_query=%E4%B9%90%E5%86%99&source=suggest'
		headers = {
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "zh-CN,zh;q=0.9",
			"cache-control": "max-age=0",
			"cookie": "cna=7JKiEpFHzlMCAd3iIOrTYAwh; t=1e17a93117f164103cc2ac78ef3512b2; tg=0; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1%26_ato%3D0; enc=%2B%2FPNvT4UOUk0ZH95RVO%2BhpnLGpENKcWFl36bVhKrsEPMiqVv%2Ff5JT0WS4sZoOwv9h9GufpldD7eX3oVR9e10cw%3D%3D; miid=7882758021902184618; hng=CN%7Czh-CN%7CCNY%7C156; tracknick=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; thw=cn; _uab_collina=156496885215409652475149; UM_distinctid=16c8876887272e-01f2bccbbcc11c-4f4c0a2e-1fa400-16c887688738fe; lgc=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; mt=ci=62_1; uc3=vt3=F8dByua36w2clPIlKf0%3D&nk2=oHTbP%2Flo5ZE%3D&id2=W8CE0v8U2F%2FX&lg2=URm48syIIVrSKA%3D%3D; uc4=id4=0%40WeNe2ZWhRAYPgRibTfzu8sc9fgA%3D&nk4=0%40oib6nB2SPAJoGEa33H5vgj%2FfwQ%3D%3D; _cc_=UIHiLt3xSw%3D%3D; _m_h5_tk=868274d6e4b085d65fd19ff53e15e079_1572431340806; _m_h5_tk_enc=09abc3253704700d25a012059769b54b; cookie2=168c9fccf3578282542dd3ae283b2434; _tb_token_=5e7e9debb746a; v=0; uc1=cookie14=UoTbnxzErJEqpw%3D%3D; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; JSESSIONID=17140734822ACF3BF310D6C7D091BD5F; l=dBOkUovPq3HTF6RKBOCaIuI8YL7T8IRVguPRwhx9i_5BW6dQAKQOkN8KzFp6cjWcM8Tp4Rb-zxwtxEn4-ylq0OpTpe1VivUHQef..; isg=BFhY9qWUsYGIKZ0HRETUxxZFKYYq6b85qVqmR5JJpBNGLfgXOlGMW24PYSO4PXSj",
			"referer": "https://www.taobao.com/",
			"upgrade-insecure-requests": "1",
			"user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
		}
		resp = requests.get(url, headers=headers)
		html = resp.text
		#print(html);
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
