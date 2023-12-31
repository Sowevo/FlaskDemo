# coding=utf-8
import os
import tempfile

import yaml
from flask import render_template, request
from werkzeug.utils import secure_filename

import utils.NotionParse as NotionParse
from models.model import db, Point
from utils.B2 import B2Uploader
from utils.JsonFlask import CustomJSONProvider, JsonFlask

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


@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World!'


@app.route('/import_notion', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return '文件缺失!'
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
            # TODO 是不是可以用db.session.add_all()来批量添加
            db.session.add(Point.from_dict(e))
        db.session.commit()
        return result
    else:
        return '数据库中已有数据!'


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


# @app.route('/addUser')
# def add_user():
#     user1 = User('张三', 'zhangsan', 'password', 1, '1111', 1)
#     user2 = User('李四', 'lisi', 'password', 0, '1111', 0)
#
#     db.session.add(user1)
#     db.session.add(user2)
#
#     db.session.commit()
#     db.session.close()
#
#     return "<p>add succssfully!"
#
#
# @app.route('/query/all')
# def query_by_all():
#     users = User.query.all()  # 查询所有数据
#     if not users:
#         return "<p>No users exist! <a href='/query/adduser'>Add users first.</a></p>"
#
#     obj = {}
#     arr = []
#     for user in users:
#         arr.append({
#             'cname': user.cname,
#             'ename': user.ename,
#             'password': user.password,
#             'is_admin': user.is_admin,
#             'company_id': user.company_id,
#             'enabled': user.enabled
#         })
#     obj['code'] = 200
#     obj['data'] = arr
#     return jsonify(obj)
#
#
# @app.route('/query/<name>')
# def query_by_name(name):
#     user = User.query.filter_by(cname=name).first()  # 查询数据
#
#     if not user:
#         return "<p>No user exist! <a href='/adduser'>Add user first.</a></p>"
#
#     obj = {
#         'cname': user.cname,
#         'ename': user.ename,
#         'password': user.password,
#         'is_admin': user.is_admin,
#         'company_id': user.company_id,
#         'enabled': user.enabled
#     }
#
#     return jsonify(obj)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
