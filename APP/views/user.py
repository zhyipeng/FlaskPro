# -*- coding: utf-8 -*-
# @Time    : 2018/9/13 0013 17:06
# @Author  : zhyipeng
# @File    : userModel.py
import os
import uuid

from flask import Blueprint, render_template, redirect, url_for, make_response, flash, request, current_app
from APP.forms import UserRegisterForm, UserLoginForm
from APP.extensions import photos, db
from PIL import Image, ImageFont, ImageFilter, ImageDraw
import random
from io import BytesIO
from APP.models import Users
from werkzeug.security import generate_password_hash, check_password_hash

user = Blueprint('user', __name__)
code_str = ''

@user.route('/index/')
def user_index():
    '''
    首页视图
    :return:
    '''
    username = request.cookies.get('username')
    photo = request.cookies.get('photo')

    return render_template('user/index.html', username=username, photo=photo)


@user.route('/logout/')
def user_logout():
    '''
    注销
    :return:
    '''
    resp = redirect(url_for('user.user_index'))
    resp.delete_cookie('username')
    resp.delete_cookie('photo')
    return resp


@user.route('/login/', methods=['GET', 'POST'])
def user_login():

    form = UserLoginForm()
    if form.validate_on_submit():
        code = form.code.data
        global code_str
        if code.lower() == code_str.lower():
            username = form.username.data
            password = form.password.data
            users = Users.query.filter(Users.username == username).first()
            if users:
                if check_password_hash(users.password, password):
                    # 登录匹配
                    resp = redirect(url_for("user.user_index"))
                    resp.set_cookie("username", username)
                    resp.set_cookie("photo", users.photo)

                    return resp
                else:
                    flash("用户名或密码错误")
            else:
                flash("用户名或密码错误")
    return render_template('user/login.html', form=form)







@user.route('/register/', methods=['GET', 'POST'])
def user_register():
    '''
    用户注册视图
    :return:
    '''

    form = UserRegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        photo = form.photo.data
        code = form.code.data
        email = form.email.data

        # 验证通过
        global code_str
        if code.lower() == code_str.lower():
            users = Users.query.filter(Users.username == username).first()
            users_for_email = Users.query.filter(Users.email == email).first()
            if users is None:
                if users_for_email is None:
                    # 保存头像
                    suffix = os.path.splitext(photo.filename)[1]
                    affix = str(uuid.uuid4())
                    new_filename = affix + suffix
                    photos.save(photo, name=new_filename)
                    # 压缩
                    img_path = os.path.join(current_app.config['UPLOADED_PHOTOS_DEST'], new_filename)
                    img = Image.open(img_path)
                    img.thumbnail((64, 64))
                    img.save(img_path)

                    # 保存到数据库
                    new_user = Users()
                    new_user.username = username
                    new_user.password = generate_password_hash(password)
                    new_user.photo = new_filename
                    new_user.email = email
                    db.session.add(new_user)

                    # 设置cookie
                    resp = redirect(url_for('user.user_index'))
                    resp.set_cookie('username', username)
                    resp.set_cookie('photo', new_filename)

                    return resp
                else:
                    flash('该邮箱已注册')
            else:
                flash('用户名已存在')
        else:
            flash('验证码错误')

    return render_template('user/register.html', form=form)


@user.route('/get_code/')
def get_code():
    '''
    验证码
    :return:
    '''
    # 生成验证吗
    global code_str
    im, code_str = validate_picture()

    buf = BytesIO()
    im.save(buf, 'jpeg')
    buf_byte = buf.getvalue()

    resp = make_response(buf_byte)

    resp.headers['Content-Type'] = 'image/jpeg'

    return resp


# 生成验证码
def validate_picture():
    '''
    生成验证码
    :return: im: Image对象; str: 验证码
    '''
    total = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345789'
    # 图片大小
    width = 130
    height = 50
    # 先生成一个图片对象
    im = Image.new('RGB', (width, height), 'white')
    # 设置字体
    font = ImageFont.truetype('simsun', 40)
    # 创建一个draw对象
    draw = ImageDraw.Draw(im)
    str = ''
    # 输出每一个文字
    for item in range(4):
        text = random.choice(total)
        str += text
        draw.text((6 + random.randint(4, 7) + 20 * item, 5 + random.randint(3, 7)), text=text, fill='black', font=font)

        # 划几根干扰线
    for num in range(4):
        x1 = random.randint(0, width / 2)
        y1 = random.randint(0, height / 2)
        x2 = random.randint(0, width)
        y2 = random.randint(height / 2, height)
        draw.line(((x1, y1), (x2, y2)), fill='black', width=1)

        # 模糊下,加个帅帅的滤镜～
    im = im.filter(ImageFilter.FIND_EDGES)
    return im, str
