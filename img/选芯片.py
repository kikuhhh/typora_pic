import requests
import json
import time 

url = 'https://so.szlcsc.com/search'

headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.56'
}


  
proxies = {'http': "socks5://127.0.0.1:7890",
           'https': "socks5://127.0.0.1:7890"}

data = {
	'os': '',
	'dp': '',
	'sb': 0,
	'pn': 0,
	'c': '',
	'k': '降压型',
	'tc': 0,
	'pds': 0,
	'pa': 0,
	'pt': 0,
	'gp': 0,
	'queryProductDiscount': '',
	'st': '',
	'sk': '降压型',
	'bp': '',
	'ep': '',
	'bpTemp': '',
	'epTemp': '',
	'stock': 'js',
	'needChooseCusType': '',
	'link-phone': '',
	'companyName': '',
	'taxpayerIdNum': '',
	'realityName': '',
	'link-phone': '',		
}

with open('芯片.txt', 'a+') as f:			
	for page in range(0, 100):
		print("Page{}".format(page))
		f.write("Page{}\n".format(page))
		data['pn'] = page
		response = requests.post(url=url, data=data, headers=headers,  proxies=proxies)
		response_dic = json.loads(response.text)
		productRecordList = response_dic['result']['productRecordList']
		for product in productRecordList:
			if '100V' in product['lightProductIntro']:
				print(product['productModel'], end='\t---->\t')
				print(product['lightProductIntro'])
				f.write(product['productModel'] + '\t---->\t')
				f.write(product['lightProductIntro'] + '\n')
		time.sleep(1)