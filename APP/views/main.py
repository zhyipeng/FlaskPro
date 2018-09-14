#-*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 17:05
# @Author  : zhyipeng
# @File    : main.py

from flask import Blueprint, render_template, redirect, url_for

main = Blueprint('main', __name__)

@main.route('/')
def root():
    return redirect(url_for('user.user_index'))

@main.route('/index/')
def index():
    return render_template('base.html')