# coding=utf-8
from flask import Flask, render_template, jsonify
from models.model import db, User
from config import config

app = Flask(__name__)
app.config.from_object(config)

db.init_app(app)
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return 'Hello World!'


@app.route('/addUser')
def add_user():
    user1 = User('张三', 'zhangsan', 'password', 1, '1111', 1)
    user2 = User('李四', 'lisi', 'password', 0, '1111', 0)

    db.session.add(user1)
    db.session.add(user2)

    db.session.commit()
    db.session.close()

    return "<p>add succssfully!"


@app.route('/query/all')
def query_by_all():
    users = User.query.all()  # 查询所有数据
    if not users:
        return "<p>No users exist! <a href='/query/adduser'>Add users first.</a></p>"

    obj = {}
    arr = []
    for user in users:
        arr.append({
            'cname': user.cname,
            'ename': user.ename,
            'password': user.password,
            'is_admin': user.is_admin,
            'company_id': user.company_id,
            'enabled': user.enabled
        })
    obj['code'] = 200
    obj['data'] = arr
    return jsonify(obj)


@app.route('/query/<name>')
def query_by_name(name):
    user = User.query.filter_by(cname=name).first()  # 查询数据

    if not user:
        return "<p>No user exist! <a href='/adduser'>Add user first.</a></p>"

    obj = {
        'cname': user.cname,
        'ename': user.ename,
        'password': user.password,
        'is_admin': user.is_admin,
        'company_id': user.company_id,
        'enabled': user.enabled
    }

    return jsonify(obj)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run()
