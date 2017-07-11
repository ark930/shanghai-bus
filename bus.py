import requests
from bs4 import BeautifulSoup


class Bus:
    def __init__(self):
        self.s = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 '
                          '(KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.10 NetType/WIFI Language/zh_CN'
        }

        self.homepage_url = 'http://shanghaicity.openservice.kankanews.com/'
        self.query_router_url = 'http://shanghaicity.openservice.kankanews.com/public/bus'
        self.query_sid_url = 'http://shanghaicity.openservice.kankanews.com/public/bus/get'
        self.query_router_details_url = 'http://shanghaicity.openservice.kankanews.com/public/bus/mes/sid/'
        self.query_stop_url = 'http://shanghaicity.openservice.kankanews.com/public/bus/Getstop'

    def print_cookies(self, cookies):
        for key in cookies.keys():
            print(key, cookies[key])

    def _homepage(self):
        r = self.s.get(self.homepage_url, headers=self.headers)

        return r

    def _query_router_page(self):
        self.headers['Referer'] = self.homepage_url
        r = self.s.get(self.query_router_url, headers=self.headers)

        return r

    def _query_sid(self, router_name):
        data = {'idnum': router_name}
        r = self.s.post(self.query_sid_url, data=data, headers=self.headers)
        sid = r.json()['sid']

        return sid

    def _query_router_details_page(self, sid, direction='0'):
        self.headers['Referer'] = self.query_router_url
        url = self.query_router_details_url + sid + '/stoptype/' + direction
        print(url)
        r = self.s.get(url, headers=self.headers)

        return r

    def _query_stop(self, sid, direction, stop_id):
        data = {'stoptype': direction, 'stopid': stop_id, 'sid': sid}
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Referer'] = self.query_router_details_url

        r = self.s.post(self.query_stop_url, data=data, headers=self.headers)

        return r

    def query_stop(self, bus_name, direction, stop_id):
        # 第一步：加载首页
        self._homepage()

        # 第二部：加载查询页面
        self._query_router_page()

        # 第三步：查询公交路线对应的sid
        sid = self._query_sid(bus_name)

        # 第四部：进入公交线路明细页面
        self._query_router_details_page(sid, direction)

        # 第五步：查询公交到站信息
        r = self._query_stop(sid, direction, stop_id)

        print(r.status_code)
        if r.status_code == 200:
            print(r.json())
        else:
            print(r.text)

        return r.json()

    def query_router(self, bus_name, direction='0'):
        # 第一步：加载首页
        self._homepage()

        # 第二部：加载查询页面
        self._query_router_page()

        # 第三步：查询公交路线对应的sid
        sid = self._query_sid(bus_name)

        # 第四部：进入公交线路明细页面
        r = self._query_router_details_page(sid, direction)

        soup = BeautifulSoup(r.text.encode(r.encoding), 'lxml')

        if direction == '0':
            stations = soup.select('div.upgoing.cur span')
            from_station = stations[0].string
            to_station = stations[1].string
        else:
            stations = soup.select('div.downgoing.cur span')
            from_station = stations[0].string
            to_station = stations[1].string

        stations = soup.select('div.station')
        routers = []
        for station in stations:
            router = {}
            for c in station.children:
                if c.name == 'span':
                    if c.attrs['class'][0] == 'num':
                        router['num'] = c.string
                    elif c.attrs['class'][0] == 'name':
                        router['name'] = c.string
            routers.append(router)

        return {
            'from': from_station,
            'to': to_station,
            'direction': direction,
            'routers': routers
        }

if __name__ == '__main__':

    bus = Bus()
    routers = bus.query_router('406路')
    print(routers)
    # r = bus.query_stop('406路', 0, '4.')

