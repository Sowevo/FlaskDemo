# coding=utf-8
import math

from models.model import BaseModel


class Resp(object):
    def __init__(self, data, code, msg):
        """
        响应对象
        :param data: 响应数据，默认为 None
        :param code: 响应代码，0 代表成功，其他 代表失败，默认为 0
        :param msg:  响应消息，默认为 'success'
        """
        self.data = data
        self.code = code
        self.msg = msg

    @classmethod
    def success(cls, data=None, code=0, msg='success'):
        """
        创建一个表示成功的响应对象

        :param data: 响应数据，默认为 None
        :param msg: 响应消息，默认为 'success'
        :param code: 响应代码，0 代表成功，其他 代表失败，默认为 0
        :return: 一个表示成功的 Resp 对象
        """
        return cls(data, code, msg)

    @classmethod
    def error(cls, data=None, code=-1, msg='error'):
        """
        创建一个表示失败的响应对象

        :param data: 响应数据，默认为 None
        :param msg: 响应消息，默认为 'fail'
        :param code: 响应代码，0 代表成功，其他 代表失败，默认为 0
        :return: 一个表示失败的 Resp 对象
        """
        return cls(data, code, msg)

    def to_dict(self):
        # 使用 vars 函数获取所有属性
        attrs = vars(self)

        for key, value in attrs.items():
            # 如果 rv 是 Model 的列表，将列表内的每个 Model 进行序列化
            if isinstance(value, list) and all(isinstance(item, BaseModel) for item in value):
                rv = [item.to_dict() for item in value]
                attrs[key] = rv
            # 如果 rv 是单个的 Model，进行序列化
            elif isinstance(value, BaseModel):
                rv = value.to_dict()
                attrs[key] = rv
        return attrs  # 这里返回的字典会包含 BaseModel 以外的所有属性


class PageResp(Resp):
    def __init__(self, data, code, msg, page, per_page, total):
        super().__init__(data, code, msg)
        # 表示当前是第几页
        self.page = page
        # 表示每页有多少条数据
        self.per_page = per_page
        # 表示总共有多少条数据
        self.total = total
        # 表示总共有多少页,动态计算
        self.total_pages = math.ceil(self.total / self.per_page)

    @classmethod
    def success(cls, data=None, code=0, msg='success', page=1, per_page=10, total=0):
        """
        创建一个表示成功的分页响应对象

        :param page:
        :param per_page:
        :param total:
        :param data: 响应数据，默认为 None
        :param msg: 响应消息，默认为 'success'
        :param code: 响应代码，0 代表成功，其他 代表失败，默认为 0
        :return: 一个表示成功的 Resp 对象
        """
        return cls(data, code, msg, page, per_page, total)
