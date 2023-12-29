# coding=utf-8
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
        return {'code': self.code, 'msg': self.msg, 'data': self.data}
