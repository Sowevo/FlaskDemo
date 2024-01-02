# -*- coding: utf-8 -*-
from datetime import datetime, date

from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider

from models.model import BaseModel
from utils.Resp import Resp


class JsonFlask(Flask):
    """
    JsonFlask类继承Flask类，并自定义make_response方法。
    使得在视图函数中可以直接返回list、dict、None或str等类型，
    并自动包装为Resp类的对象转化为JSON格式的HTTP响应。
    """

    def make_response(self, rv):
        """
        重写make_response方法
        对于视图函数返回的数据进行处理
        如果是Model实例或实例列表，先进行序列化，再用Resp.success方法封装一下
        :param rv:
        :return:
        """
        # 如果rv是Model列表，先对每个实例进行序列化
        if isinstance(rv, list) and all(isinstance(item, BaseModel) for item in rv):
            rv = [item.to_dict() for item in rv]
        # 如果rv是单个的Model，进行序列化
        elif isinstance(rv, BaseModel):
            rv = rv.to_dict()

        # 如果rv是字典或者列表（也即是已经序列化的实例或实例列表），用Resp.success方法封装一下
        if rv is None or isinstance(rv, (list, dict)):
            rv = Resp.success(rv)
        # 如果是Resp对象，转化为可以用于HTTP响应的JSON格式
        if isinstance(rv, Resp):
            rv = jsonify(rv.to_dict())
        # 返回封装后的HTTP响应
        return super().make_response(rv)


class CustomJSONProvider(DefaultJSONProvider):
    """
    自定义json序列化
    改变了jsonify中对datetime和date的序列化方式
    """

    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return super().default(obj)
