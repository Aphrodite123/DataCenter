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
		url = 'https://s.taobao.com/search?ie=utf8&initiative_id=staobaoz_20191029&stats_click=search_radio_all%3A1&js=1&imgfile=&q=%E6%9C%89%E9%81%93%E4%BA%91%E7%AC%94%E8%AE%B0%E7%AC%94&suggest=history_2&_input_charset=utf-8&wq=%E6%9C%89%E9%81%93%E4%BA%91%E7%AC%94%E8%AE%B0&suggest_query=%E6%9C%89%E9%81%93%E4%BA%91%E7%AC%94%E8%AE%B0&source=suggest'
		headers = {
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
			"cache-control": "max-age=0",
			"cookie": "thw=cn; cna=/GY4FpwqRg4CAd3iIOqQQqo9; v=0; t=9cd6eb78bf16caca599d0e108467187a; cookie2=7a9b261ea99138c455d18c733808258e; _tb_token_=3b85ebef1b3ee; unb=899977127; uc3=lg2=W5iHLLyFOGW7aA%3D%3D&id2=W8CE0v8U2F%2FX&vt3=F8dByua36wxPYVIsTJs%3D&nk2=oHTbP%2Flo5ZE%3D; csg=197d3de3; lgc=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; cookie17=W8CE0v8U2F%2FX; dnk=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; skt=60f8f43fc213ff49; existShop=MTU3MjQxNDQ0NA%3D%3D; uc4=id4=0%40WeNe2ZWhRAYPgRibTfzu8sY5qz4%3D&nk4=0%40oib6nB2SPAJoGEa33H5vg%2B8JCQ%3D%3D; tracknick=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; _cc_=UtASsssmfA%3D%3D; tg=0; _l_g_=Ug%3D%3D; sg=%E5%A7%AC71; _nk_=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; cookie1=U%2BGWngd%2FhfSbx9oeCKJj37j1xapM4es%2BPmPCtgIAF3k%3D; mt=ci=62_1; enc=sOeVbbaz%2Fx8mqGAKtJy38GOLJe9OymxsLWV0JI8XDPvgzsb8WNkjvPNwtXUOCqAIak8CsAoA4q86AtwcsbDI7A%3D%3D; _uab_collina=157241449341132849359094; alitrackid=www.taobao.com; lastalitrackid=www.taobao.com; hng=CN%7Czh-CN%7CCNY%7C156; x5sec=7b227365617263686170703b32223a22346337346234623561306533613538633832386530633333383136626633636643506a4b354f3046454c75392f7044457059433349526f4d4f446b354f5463334d5449334f7a6777227d; uc1=cookie15=URm48syIIVrSKA%3D%3D&cookie14=UoTbnxzN%2FboEWw%3D%3D; JSESSIONID=CC12C8EEEDBE058C8BE834F65441696E; l=dBamKw8gq3F0g_jEBOCwourza77OSIRAguPzaNbMi_5wC6L64CQOkN6XTFp6VjWfTOLB4-ERe5p9-eteiKy06Pt-g3fPaxDc.; isg=BCYmjEX6RwhE-BOsY-Fx-TTod5WoB2rBEX8dAhDPEskkk8ateJe60Qxh78-6O2LZ",
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
