import requests
import json


def print_cookies(cookies):
    for key in cookies.keys():
        print(key, cookies[key])

        
s = requests.Session()

headers = {}
headers['User-Agent'] = 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.10 NetType/WIFI Language/zh_CN'

# 第一步：加载首页
url1 = 'http://shanghaicity.openservice.kankanews.com/'
r = s.get(url1, headers = headers)
#print_cookies(r.cookies)
#print('\n')

# 第二部：加载查询页面
url2 = 'http://shanghaicity.openservice.kankanews.com/public/bus'
headers['Referer'] = url1
r = s.get(url2, headers = headers)
#print_cookies(r.headers)
#print_cookies(r.cookies)

# 第三步：查询公交路线对应的sid
url3 = 'http://shanghaicity.openservice.kankanews.com/public/bus/get'
data = {'idnum':'406路'}
r = s.post(url3, data = data, headers = headers)
sid = r.json()['sid']

# 第四部：进入公交线路明细页面
url4 = 'http://shanghaicity.openservice.kankanews.com/public/bus/mes/sid/'
url4 = url4 + sid
headers['Referer'] = url2
r = s.get(url4, headers = headers)
#print('\n')
#print_cookies(r.cookies)

# 第五步：查询公交到站信息
url5 = 'http://shanghaicity.openservice.kankanews.com/public/bus/Getstop'
data = {'stoptype': 0, 'stopid': '4.', 'sid': sid}
headers['Content-Type'] = 'application/x-www-form-urlencoded'
headers['Referer'] = url4
r = s.post(url5, data = data, headers = headers)

print(r.status_code)
if r.status_code == 200:
    print(r.json())
else:
    print(r.text)

