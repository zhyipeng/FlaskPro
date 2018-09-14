#-*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 16:56
# @Author  : zhyipeng
# @File    : extensions.py

from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

bootstrap = Bootstrap()

photos = UploadSet('photos', IMAGES)

db = SQLAlchemy()

migrate = Migrate()


def extensions_config(app):
    '''
    管理扩展插件
    :param app: app名
    :return: None
    '''

    bootstrap.init_app(app)

    configure_uploads(app, photos)
    patch_request_class(app, size=1024 * 1024)

    db.init_app(app)
    migrate.init_app(app, db=db)