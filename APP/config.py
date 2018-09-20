# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 16:49
# @Author  : zhyipeng
# @File    : config.py

import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config(object):
    '''
    基本配置
    '''
    # 密钥
    SECRET_KEY = 'hohov#@Hnopoi#$#on2'

    MAX_CONTENT_LENGTH = 1024 * 1024
    # 上传集名
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'APP\\static\\image')

    # 忽略警告
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 自动提交
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    # 邮件服务器
    MAIL_SERVER = 'smtp.aliyun.com'
    MAIL_USERNAME = 'zhyipeng@aliyun.com'
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_PASSWORD = 'Zhang789'

    # 调试模式
    DEBUG = True
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class DevelopmentConfig(Config):
    '''
    开发环境配置
    '''
    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/flaskpro'
    pass


class TestConfig(Config):
    '''
    测试环境配置
    '''

    pass


# 数据库配置字典
DATABASE_CONFIG = {
    'database_name': 'mysql',
    'database_drive': 'pymysql',
    'username': 'root',
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': '127.0.0.1',
    'port': os.getenv('MYSQL_PORT'),
    'database': 'flask'
}


class ProductConfig(Config):
    '''
    发布环境配置
    '''
    SQLAHCHEMY_DATABASE_URI = '{database_name}+{database_drive}://{username}:{password}@{host}:{port}/{database}'.format(
        **DATABASE_CONFIG)
    pass


config = {
    'default': DevelopmentConfig,
    'development': DevelopmentConfig,
    'test': TestConfig,
    'product': ProductConfig
}
