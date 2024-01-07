# coding=utf-8
import os
import tempfile

import yaml
from flask import render_template, request, redirect, url_for
from sqlalchemy import desc, asc
from werkzeug.utils import secure_filename

import utils.NotionParse as NotionParse
from models.model import db, Point, City
from utils import ExcelParse
from utils.B2 import B2Uploader
from utils.JsonFlask import CustomJSONProvider, JsonFlask
from utils.Resp import PageResp, Resp

app = JsonFlask(__name__)
# 读取配置文件
with open('config.yaml') as config_file:
    config = yaml.safe_load(config_file)
app.config.update(config)
# 自定义json序列化
app.json = CustomJSONProvider(app)

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('index'))


@app.route('/index.html', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/detail/<id>.html', methods=['GET'])
def detail(id):
    point = Point.query.filter_by(id=id).first()
    if point:
        return render_template('detail.html', data=point)
    else:
        return render_template('404.html'), 404


@app.route('/import_notion', methods=['POST'])
def import_notion():
    if 'file' not in request.files:
        return Resp.error(msg='文件缺失!')
    file = request.files['file']
    filename = secure_filename(file.filename)
    # 如果数据库中没有数据，才执行解析与添加
    count = Point.query.count()
    if count <= 0:
        with tempfile.TemporaryDirectory() as tmp_dirname:
            save_path = os.path.join(tmp_dirname, filename)
            file.save(save_path)
            result = NotionParse.parse(save_path)
        for e in result:
            db.session.add(Point.from_dict(e))
        db.session.commit()
        return result
    else:
        return Resp.error(msg='数据库中已有数据!')


@app.route('/import_city', methods=['POST'])
def import_city():
    if 'file' not in request.files:
        return Resp.error(msg='文件缺失!')
    file = request.files['file']
    filename = secure_filename(file.filename)
    # 如果数据库中没有数据，才执行解析与添加
    count = City.query.count()
    if count <= 0:
        with tempfile.TemporaryDirectory() as tmp_dirname:
            save_path = os.path.join(tmp_dirname, filename)
            file.save(save_path)
            result = ExcelParse.parse(save_path)
        for e in result:
            db.session.add(City.from_dict(e))
        db.session.commit()
        return result
    else:
        return Resp.error(msg='数据库中已有数据!')


@app.route('/upload_image', methods=['POST'])
def upload_image():
    """
    上传图片
    :return:
    """
    if 'file' not in request.files:
        return '文件缺失!'
    file = request.files['file']
    filename = secure_filename(file.filename)
    with tempfile.TemporaryDirectory() as tmpdirname:
        save_path = os.path.join(tmpdirname, filename)
        file.save(save_path)
        path = B2Uploader().upload_file(save_path)
    return path


@app.route('/point/all', methods=['POST'])
def all_points():
    """
    获取所有景点
    :return:
    """
    if not request.is_json:
        return Resp.error(msg='请求参数错误')

    data = request.get_json()
    page = data.get('page', 1)  # 从请求参数中获取当前页数，默认为第一页
    limit = data.get('limit', 10)  # 从请求参数中获取每页的数量，默认为10
    order_field = data.get('field', None)
    order = data.get('order', None)

    query = Point.query

    # 根据排序规则进行排序
    if order_field and order:
        if order == 'desc':
            query = query.order_by(desc(getattr(Point, order_field)))
        else:
            query = query.order_by(asc(getattr(Point, order_field)))

    points = query.paginate(page=page,
                            per_page=limit,
                            max_per_page=1000,
                            error_out=False
                            )
    return PageResp.success(data=points.items, count=points.total)


@app.route('/point/add', methods=['POST'])
def add_point():
    if not request.is_json:
        return Resp.error(msg='请求参数错误')
    # TODO 要加校验么???
    data = request.get_json()
    point = Point.from_dict(data)
    db.session.add(point)
    db.session.commit()
    return point


@app.route('/city/list', methods=['POST'])
def list_city():
    if not request.is_json:
        return Resp.error(msg='请求参数错误')
    data = request.get_json()
    parent = data.get('parent', '')
    _type = data.get('type', 'country')
    if _type == 'country':
        query = City.query.filter(City.state.is_(None))
        cities = query.all()
        # 转换为字典,只要code和name
        cities = [{'code': c.code, 'name': c.country} for c in cities]
    elif _type == 'state':
        query = City.query.filter(City.city.is_(None))
        if parent:
            query = query.filter_by(country=parent)
        cities = query.all()
        # 转换为字典,只要code和name
        cities = [{'code': c.code, 'name': c.state} for c in cities]
    elif _type == 'city':
        query = City.query.filter(City.city.isnot(None))
        if parent:
            query = query.filter_by(state=parent)
        cities = query.all()
        # 转换为字典,只要code和name
        cities = [{'code': c.code, 'name': c.city} for c in cities]
    else:
        cities = []
    return cities


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(port=3333)
