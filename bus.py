import requests
import pickle
import os
import time
from bs4 import BeautifulSoup
from bus_routers import Routers
from InvalidParameterException import InvalidParameterException
import logging
import json
import datetime


class Bus:
    def __init__(self):
        logging.basicConfig(filename='logger.log', level=logging.INFO)

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

        logging.info('')
        logging.info('Time: ' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        logging.info('Request: ' + json.dumps(data))
        logging.info('Response: ' + r.text)

        return r

    def _init_request(self, router_name):
        self._check_routers(router_name)

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

        # 第三步：查询公交路线对应的sid
        sid = self._query_sid(router_name)

        return sid

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

    def _check_routers(self, router_name):
        if router_name not in Routers:
            raise InvalidParameterException('router_not_exists', '不存在该公交线路', 400)

    def query_stop(self, router_name, direction, stop_id):
        sid = self._init_request(router_name)

        # 查询公交到站信息
        r = self._query_stop(sid, direction, stop_id)

        res = r.json()
        if type(res) is list:
            res = res[0]
            return {
                'router_name': res['@attributes']['cod'],
                'direction': direction,
                'plate_number': res['terminal'],
                'stop_interval': res['stopdis'],
                'distance': res['distance'],
                'time': res['time'],
                'status': 'running'
            }
        else:
            return {
                'router_name': router_name,
                'direction': direction,
                'plate_number': '',
                'stop_interval': '',
                'distance': '',
                'time': '',
                'status': 'waiting'
            }

    def query_router(self, router_name, direction='0'):
        self.sid = self._init_request(router_name)

        # 进入公交线路明细页面
        r = self._query_router_details_page(self.sid, direction)

        soup = BeautifulSoup(r.text.encode(r.encoding), 'lxml')

        if direction == '0':
            stations = soup.select('div.upgoing.cur span')
            from_station = stations[0].string
            to_station = stations[1].string

            strat_at = soup.select('div.upgoing.cur em.s')[0].string
            end_at = soup.select('div.upgoing.cur em.m')[0].string
        else:
            stations = soup.select('div.downgoing.cur span')
            from_station = stations[0].string
            to_station = stations[1].string

            strat_at = soup.select('div.downgoing.cur em.s')[0].string
            end_at = soup.select('div.downgoing.cur em.m')[0].string

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
            'start_at': strat_at,
            'end_at': end_at,
            'direction': direction,
            'stops': stops
        }

    def query_router_details(self, router_name, direction='0'):
        router = self.query_router(router_name, direction)

        stops = router['stops']

        for stop in stops:
            # 查询公交到站信息
            r = self._query_stop(self.sid, direction, stop['stop_id'])

            res = r.json()
            if type(res) is list:
                res = res[0]
                stop['plate_number'] = res['terminal']
                stop['stop_interval'] = res['stopdis']
                stop['distance'] = res['distance']
                stop['time'] = res['time']
                stop['status'] = 'running'
            else:
                stop['plate_number'] = ''
                stop['stop_interval'] = ''
                stop['distance'] = ''
                stop['time'] = ''
                stop['status'] = 'waiting'

        return router


if __name__ == '__main__':
    router_name = '406路'
    direction = '0'
    stop_id = '4'

    bus = Bus()
    stops = bus.query_router(router_name)
    print(stops)

    r = bus.query_stop(router_name, direction, stop_id)
    print(r)

    r = bus.query_router_details(router_name, direction)
    print(r)
