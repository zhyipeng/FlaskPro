#-*- coding: utf-8 -*-
# @Time    : 2018/9/14 0014 16:39
# @Author  : zhyipeng
# @File    : userModel.py

from APP.extensions import db

class Users(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(32), unique=True)
    photo = db.Column(db.String(128))
