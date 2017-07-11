import requests
import pickle
import os
import time
from bs4 import BeautifulSoup


class Bus:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 '
                          '(KHTML, like Gecko) Mobile/14F89 MicroMessenger/6.5.10 NetType/WIFI Language/zh_CN'
        }

        self.homepage_url = 'http://shanghaicity.openservice.kankanews.com/'
        self.query_router_url = 'http://shanghaicity.openservice.kankanews.com/public/bus'
        self.query_sid_url = 'http://shanghaicity.openservice.kankanews.com/public/bus/get'
        self.query_router_details_url = 'http://shanghaicity.openservice.kankanews.com/public/bus/mes/sid/'
        self.query_stop_url = 'http://shanghaicity.openservice.kankanews.com/public/bus/Getstop'

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
        r = self.s.get(url, headers=self.headers)

        return r

    def _query_stop(self, sid, direction, stop_id):
        data = {'stoptype': direction, 'stopid': stop_id, 'sid': sid}
        self.headers['Content-Type'] = 'application/x-www-form-urlencoded'
        self.headers['Referer'] = self.query_router_details_url

        r = self.s.post(self.query_stop_url, data=data, headers=self.headers)

        return r

    def _init_request(self):
        if os.path.exists('session.log'):
            with open('session.log', 'rb') as f:
                session = pickle.load(f)

                if session['expired_at']+1800 < time.time():
                    # session expired
                    self._make_session()
                else:
                    # read session from cache
                    self.s = session['session']

        else:
            # session not exists
            self._make_session()

    def _make_session(self):
        self.s = requests.Session()

        # 第一步：加载首页
        self._homepage()

        # 第二部：加载查询页面
        self._query_router_page()

        with open('session.log', 'wb') as f:
            session = {
                'session': self.s,
                'expired_at':  time.time()
            }
            pickle.dump(session, f)

    def query_stop(self, bus_name, direction, stop_id):
        self._init_request()

        # 第三步：查询公交路线对应的sid
        sid = self._query_sid(bus_name)

        # 第四部：进入公交线路明细页面
        self._query_router_details_page(sid, direction)

        # 第五步：查询公交到站信息
        r = self._query_stop(sid, direction, stop_id)

        # print(r.status_code)
        # if r.status_code == 200:
        #     print(r.json())
        # else:
        #     print(r.text)

        res = r.json()[0]

        return {
            'router_name': res['@attributes']['cod'],
            'direction': direction,
            'plate_number': res['terminal'],
            'stop_at': res['stopdis'],
            'distance': res['distance'],
            'time': res['time'],
        }

    def query_router(self, bus_name, direction='0'):
        self._init_request()

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
        stops = []
        for station in stations:
            router = {}
            for c in station.children:
                if c.name == 'span':
                    if c.attrs['class'][0] == 'num':
                        router['stop_id'] = c.string
                    elif c.attrs['class'][0] == 'name':
                        router['stop_name'] = c.string
            stops.append(router)

        return {
            'from': from_station,
            'to': to_station,
            'direction': direction,
            'stops': stops
        }

if __name__ == '__main__':

    bus = Bus()
    stops = bus.query_router('406路')
    print(stops)
    # r = bus.query_stop('406路', 0, '4.')

