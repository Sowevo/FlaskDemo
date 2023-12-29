# -*- coding: utf-8 -*-
from datetime import datetime, date

from flask import Flask, jsonify
from flask.json.provider import DefaultJSONProvider

from utils.Resp import Resp


class JsonFlask(Flask):
    """
    JsonFlask类继承Flask类，并自定义make_response方法。
    使得在视图函数中可以直接返回list、dict、None或str等类型，
    并自动包装为Resp类的对象转化为JSON格式的HTTP响应。
    """

    def make_response(self, rv):
        """重写Flask的make_response方法。
        rv是视图函数的返回值。
        如果rv是None或者是list、dict、str，
        会调用Resp的success方法将其转化为Resp对象。
        如果rv是Resp对象，会调用其to_dict方法将其转化为dict，
        然后通过jsonify将其转化为JSON格式的HTTP响应。
        最后，如果以上需求都不符合，即返回值已经是可以直接转化为HTTP响应的类型，
        或者是Response对象，则直接调用父类(Flask)原本的make_response方法处理返回值。
        """
        if rv is None or isinstance(rv, (list, dict, str)):
            rv = Resp.success(rv)

        if isinstance(rv, Resp):
            rv = jsonify(rv.to_dict())

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
