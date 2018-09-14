#-*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 17:25
# @Author  : zhyipeng
# @File    : userForms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from flask_wtf.file import FileAllowed, FileRequired, FileField

ALLOW_PHOTOS = ['jpg', 'png', 'jpeg', 'bmp']

class UserRegisterForm(FlaskForm):
    '''
    用户注册表单，用户名，密码，重复密码，邮箱，验证码，头像
    '''

    username = StringField(label='用户名', validators=[DataRequired(message='用户名不能为空')])
    password = PasswordField(label='密码', validators=[DataRequired(message='密码不能为空'),
                                                     Length(min=6, max=18, message='请输入6-18位密码')])
    re_password = PasswordField(label='确认密码', validators=[DataRequired(message='请确认密码'),
                                                          EqualTo('password', message='两次密码不一致')])
    email = StringField(label='邮箱', validators=[DataRequired(message='邮箱不能为空'),
                                                Email(message='邮箱格式不正确')])
    code = StringField(label='验证码', validators=[DataRequired(message='请输入验证码')])
    photo = FileField(label='头像', validators=[FileRequired(message='请选择要上传的文件'),
                                              FileAllowed(ALLOW_PHOTOS, message='无法识别的图片格式')])
    submit = SubmitField(label='注册')

class UserLoginForm(FlaskForm):
    '''
    用户登录表单，用户名，密码，验证码
    '''

    username = StringField(label='用户名', validators=[DataRequired(message='用户名不能为空')])
    password = PasswordField(label='密码', validators=[DataRequired(message='密码不能为空')])
    code = StringField(label='验证码', validators=[DataRequired(message='请输入验证码')])
    submit = SubmitField(label='登录')