#-*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 16:45
# @Author  : zhyipeng
# @File    : manage.py

from flask_script import Manager
from APP import create_app
from flask_migrate import MigrateCommand
from APP.extensions import db
import os

config_name = os.getenv('CONFIG_NAME') or 'default'

app = create_app(config_name)
manager = Manager(app)

@manager.command
def create():
    db.create_all()
    return '表创建成功'


# 添加命令
manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()

