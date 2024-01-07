# -*- coding: utf-8 -*-
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class BaseModel(db.Model):
    __abstract__ = True  # 声明这是一个抽象类，不会创建表

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    @classmethod
    def from_dict(cls, data):
        """
        添加类方法用于从字典创建对象
        :param data:
        :return:
        """
        allowed_keys = set(cls.__init__.__code__.co_varnames[1:])  # 获取 __init__ 方法参数名集合
        keys_to_remove = [k for k in data.keys() if k not in allowed_keys]  # 确定要在 data 字典中移除的键

        for k in keys_to_remove:
            del data[k]  # 从 data 字典中移除不存在的键/参数

        return cls(**data)


class Point(BaseModel):
    __tablename__ = 'point'

    # 以下是表的字段
    id = db.Column(db.Integer, primary_key=True)
    # 名字
    name = db.Column(db.String(60))
    # 国家
    country = db.Column(db.String(60))
    # 城市
    city = db.Column(db.String(60))
    # 省份
    state = db.Column(db.String(60))
    # 备注
    remarks = db.Column(db.String(200))
    # 舞台
    stage = db.Column(db.String(60))
    # 门票
    ticket = db.Column(db.String(60))
    # 坐标
    coordinates = db.Column(db.String(60))
    # 耗时
    duration = db.Column(db.String(60))
    # google地图链接
    google_map_url = db.Column(db.String(200))
    # google街景链接
    google_street_view_url = db.Column(db.String(300))
    # 附近车站google链接
    google_station_url = db.Column(db.String(200))
    # 图片链接
    images = db.Column(db.String(500))
    # 最后更新时间
    last_update = db.Column(db.DateTime, default=datetime.now)
    # 创建时间
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, city, coordinates, country, duration, google_map_url, google_street_view_url, images,
                 name, remarks, stage, state, google_station_url, ticket):
        self.city = city
        self.coordinates = coordinates
        self.country = country
        self.duration = duration
        self.google_map_url = google_map_url
        self.google_street_view_url = google_street_view_url
        self.images = ','.join(images) if isinstance(images, list) else images  # 添加这行代码
        self.name = name
        self.remarks = remarks
        self.stage = stage
        self.state = state
        self.google_station_url = google_station_url
        self.ticket = ticket

    @property
    def images_list(self):
        return self.images.split(',') if self.images else []


class City(BaseModel):
    """
    城市表
    目前有国家、省份、城市三个字段
    如果省份为空，则表示是个国家
    如果城市为空，则表示是个省份
    如果城市不为空，则表示是个城市
    """
    __tablename__ = 'city'

    # 以下是表的字段
    id = db.Column(db.Integer, primary_key=True)
    # 国家
    country = db.Column(db.String(60))
    # 城市
    city = db.Column(db.String(60))
    # 省份
    state = db.Column(db.String(60))
    # 排序
    sort = db.Column(db.Integer, default=0)

    def __init__(self, country, city, state, sort=0):
        self.country = country
        self.city = city
        self.state = state
        self.sort = sort
