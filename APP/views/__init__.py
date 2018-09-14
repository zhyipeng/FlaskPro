#-*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 16:49
# @Author  : zhyipeng
# @File    : __init__.py.py

from .user import user
from .main import main

BLUEPRINTS = (
    (user, '/user'),
    (main, '')
)


def blueprint_config(app):
    '''
    蓝本配置
    :param app: app名
    :return: None
    '''
    for blueprint, prefix in BLUEPRINTS:
        app.register_blueprint(blueprint, url_prefix=prefix)