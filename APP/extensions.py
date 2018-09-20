#-*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 16:56
# @Author  : zhyipeng
# @File    : extensions.py

from flask_bootstrap import Bootstrap
from flask_uploads import UploadSet, IMAGES, configure_uploads, patch_request_class
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension


# 实例一个用户管理
login_manager = LoginManager()
# 登录端点
login_manager.login_view = 'user.user_login'
# 登录提示
login_manager.login_message = '请登录'
# session保护
login_manager.session_protection = 'strong'

bootstrap = Bootstrap()

photos = UploadSet('photos', IMAGES)

db = SQLAlchemy()

migrate = Migrate()

mail = Mail()

debugtoolbar = DebugToolbarExtension()


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

    mail.init_app(app)

    debugtoolbar.init_app(app)

    login_manager.init_app(app)