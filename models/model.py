# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'eis_user'
    id = db.Column(db.Integer, primary_key=True)
    cname = db.Column(db.String(255))
    ename = db.Column(db.String(255))
    password = db.Column(db.String(255))
    is_admin = db.Column(db.Integer)
    company_id = db.Column(db.String(255))
    enabled = db.Column(db.Integer)

    def __init__(self, cname, ename, password, is_admin, company_id, enabled):
        self.cname = cname
        self.ename = ename
        self.password = password
        self.is_admin = is_admin
        self.company_id = company_id
        self.enabled = enabled
