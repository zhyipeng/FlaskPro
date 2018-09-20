#-*- coding: utf-8 -*-
# @Time    : 2018/9/14 0014 16:39
# @Author  : zhyipeng
# @File    : userModel.py

from APP.extensions import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature
from flask import current_app, flash
from flask_login import UserMixin

class Users(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True, autoincrement=True)

    username = db.Column(db.String(32), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(32), unique=True)
    photo = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=0)
    is_delete = db.Column(db.Boolean, default=0)

    @property
    def password(self):
        raise AttributeError('密码不可读')

    @password.setter
    def password(self, psw):
        self.password_hash = generate_password_hash(psw)

    def check_password(self, psw):
        '''
        密码校验
        :param psw: 输入的密码
        :return: bool
        '''
        return check_password_hash(self.password_hash, psw)

    def generate_token(self, expires=3600):
        '''
        生成token
        :param expires: 有效时间
        :return: token
        '''

        s = Serializer(secret_key=current_app.config['SECRET_KEY'], expires_in=expires)
        return s.dumps({'id': self.id})


    @staticmethod
    def user_active(token):
        '''
        用户激活
        :param token: 会话
        :return: bool
        '''

        s = Serializer(secret_key=current_app.config['SECRET_KEY'])

        # 校验token
        try:
            data = s.loads(token)
        # 是否过期
        except SignatureExpired:
            flash('该链接已过期，请重新申请')
            return False
        # 是否被篡改
        except BadSignature:
            flash('该链接无效，请重新申请')
            return False

        user = Users.query.get(int(data.get('id')))
        if user:
            if user.is_active:
                flash('该用户已激活')
            else:
                user.is_active = True
                db.session.add(user)
                flash('激活成功')
        else:
            flash('该用户不存在，请重新申请')

        return True

# login_manager 登录回调
@login_manager.user_loader
def load_user(uid):
    return Users.query.get(int(uid))