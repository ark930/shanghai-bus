from sqlalchemy import Column, String, Integer, Enum, TIMESTAMP
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Stop(Base):
    __tablename__ = 'stops'

    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, index=True)
    router_name = Column(String(20))
    stop_id = Column(Integer)
    stop_name = Column(String(20))
    direction = Column(Enum('up', 'down'))
    plate_number = Column(String(10))
    distance = Column(Integer)
    status = Column(Enum('running', 'waiting'))
    stop_interval = Column(Integer)
    time = Column(Integer)
    created_at = Column(TIMESTAMP)


if __name__ == '__main__':
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    # 初始化数据库连接
    engine = create_engine('mysql+pymysql://root:@localhost:3306/shanghai_bus?charset=utf8', echo=True)

    # 创建 Session:
    Session = sessionmaker(bind=engine)
    session = Session()

    # 创建 Table
    Base.metadata.create_all(engine)

    # 插入数据
    stop = Stop(router_name='406路')
    session.add(stop)
    session.commit()
