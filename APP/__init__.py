#-*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 16:46
# @Author  : zhyipeng
# @File    : __init__.py.py

from flask import Flask
from APP.extensions import extensions_config
from APP.views import blueprint_config
from APP.config import config
from APP.models import *


def create_app(config_name):
    '''
    创建app
    :param config_name: 环境名
    :return: Flask app对象
    '''
    app = Flask(__name__)

    app.config.from_object(config.get(config_name))

    # 配置插件
    extensions_config(app)

    # 配置蓝本
    blueprint_config(app)

    return app