import datetime
import time

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from bus import Bus
from stop import Stop


class Record:
    def bus_info(self, router_name, direction):
        bus = Bus()
        routers = bus.query_router_details(router_name, direction)

        Base = declarative_base()

        # 初始化数据库连接
        engine = create_engine('mysql+pymysql://root:@localhost:3306/shanghai_bus?charset=utf8', echo=True)

        # 创建 Session:
        Session = sessionmaker(bind=engine)
        session = Session()

        # 创建 Table
        Base.metadata.create_all(engine)

        group_id = int(time.time())
        direction = 'up' if routers['direction'] == '0' else 'down'
        stops = routers['stops']

        for s in stops:
            distance = None if s['distance'] == '' else s['distance']
            stop_interval = None if s['stop_interval'] == '' else s['stop_interval']
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

    record = Record()
    record.bus_info(router_name, '0')
    time.sleep(1)
    record.bus_info(router_name, '1')




