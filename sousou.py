# -*- coding:utf-8 -*-
# Create @ 2019-06-21 16:51:51
# Author @ 819070918@qq.com

import re
import sys
import csv
import json
import time
import requests
import imp
from xlwt import Workbook

imp.reload(sys)

size = 44
page_num = 10

def parse_title(title):
	title = title.replace("<span class=H>", "")
	title = title.replace("</span>", "")
	return title


def parse_count(count):
	c = 10000 if "万" in count else 1
	count = re.findall(r"\d+\.?\d*", count)
	return float(count[0])*c
	
def write_file(content):
    f = open("text.txt",'wb')
    f.write(content) 
    f.close()

def main(word):
	data = [["名称", "价格", "销量", "链接"]]
	for i in range(page_num):
		url = 'https://s.taobao.com/search?q=%E6%97%A9%E6%95%99%E6%9C%BA%E5%99%A8%E4%BA%BA&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306&cps=yes&ppath=20000%3A12608401'
		headers = {
			"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
			"accept-encoding": "gzip, deflate, br",
			"accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
			"cache-control": "max-age=0",
			"cookie": "cna=7JKiEpFHzlMCAd3iIOrTYAwh; _med=dw:1920&dh:1080&pw:1920&ph:1080&ist:0; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; x=__ll%3D-1%26_ato%3D0; _uab_collina=155313863395410561211321; cq=ccp%3D1; hng=CN%7Czh-CN%7CCNY%7C156; enc=%2B%2FPNvT4UOUk0ZH95RVO%2BhpnLGpENKcWFl36bVhKrsEPMiqVv%2Ff5JT0WS4sZoOwv9h9GufpldD7eX3oVR9e10cw%3D%3D; uc1=cookie14=UoTaHY72d1UC%2Fw%3D%3D; t=1e17a93117f164103cc2ac78ef3512b2; uc3=vt3=F8dBy3%2F51BmKcLtvaJ8%3D&id2=W8CE0v8U2F%2FX&nk2=oHTbP%2Flo5ZE%3D&lg2=WqG3DMC9VAQiUQ%3D%3D; tracknick=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; lgc=%5Cu68A6%5Cu5FC6%5Cu7F8E%5Cu59EC; _tb_token_=e16711699b5eb; cookie2=1dba826b2e89942e5642db7cbc41eab3; _m_h5_tk=f0a29c3980105a4fa2146d9306f518d0_1565152879735; _m_h5_tk_enc=a7513f89428e3b4682d74d96db663628; swfstore=271965; res=scroll%3A1903*2588-client%3A1903*969-offset%3A1903*2588-screen%3A1920*1080; pnm_cku822=098%23E1hvipvUvbpvUpCkvvvvvjiPRF5h6jYRRLsptjnEPmPvgjE2nLqO0jiEn2SO1j38n8wCvvpvvUmmRphvCvvvvvmivpvUvvmvnk5l1O%2FEvpvVmvvC9jamKphv8vvvvvCvpvvvvvm2phCv2mwvvUnvphvpgvvv96CvpCCvvvm2phCvhhvEvpCWmmHovvwz1b2XSfpAOH2%2BFOcn%2B3C1BJFEDaVTRogRD7zvaXTAVAilKbVxnqW6cbmxfaAK5kx%2FAj7ZD46OjLVxfw3l5dUf857gF4VQRphCvvOvCvvvphvPvpvhvvvvvv%3D%3D; l=cBQayX6RvoYUQvroKOCN5uI8Yg7TQIRAguPRwhf6i_5LU6Y_5k7Ok5zeQFv6cjWd9SYB4XOjjVJ9-etktEpTY-cHtBUV.; isg=BAEBeIRYOBo7ClNAfxdMrGPfEE3bhnbM724RLWNW54hnSiEcq3xc8C9AKP6pwg1Y",
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
