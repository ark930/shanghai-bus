import datetime
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bus import Bus
from stop import Stop


class Record:
    def bus_info(self, router_name, direction, group_id):
        bus = Bus()
        routers = bus.query_router_details(router_name, direction)
        stops = routers['stops']

        # 全线停运后，不记录到数据库
        for s in stops:
            if s['status'] == 'running':
                break
        else:
            return

        Base = declarative_base()

        # 初始化数据库连接
        engine = create_engine('mysql+pymysql://root:@localhost:3306/shanghai_bus?charset=utf8', echo=True)

        # 创建 Session:
        Session = sessionmaker(bind=engine)
        session = Session()

        # 创建 Table
        Base.metadata.create_all(engine)

        direction = 'up' if routers['direction'] == '0' else 'down'

        # 删除无效的的数据
        if stops[0]['plate_number'] == stops[1]['plate_number']:
            del stops[1]

        for s in stops:
            stop_interval = None if s['stop_interval'] == '' else s['stop_interval']

            # 过滤不需要记录的站点
            if stop_interval != '1':
                continue

            distance = None if s['distance'] == '' else s['distance']
            times = None if s['time'] == '' else s['time']
            plate_number = None if s['plate_number'] == '' else s['plate_number']

            stop = Stop(group_id=group_id, router_name=router_name, direction=direction, stop_id=s['stop_id'],
                        stop_name=s['stop_name'], plate_number=plate_number, distance=distance,
                        status=s['status'], stop_interval=stop_interval, time=times,
                        created_at=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            session.add(stop)

        session.commit()


if __name__ == '__main__':
    router_name = '406路'

    group_id = int(time.time())

    record = Record()
    record.bus_info(router_name, '0', group_id)
    record.bus_info(router_name, '1', group_id)




