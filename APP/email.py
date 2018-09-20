#-*- coding: utf-8 -*-
# @Time    : 2018/9/19 0019 19:42
# @Author  : zhyipeng
# @File    : email.py

from APP.extensions import mail
from flask_mail import Message
from flask import current_app, render_template
import threading


# 异步执行
def async_send_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(subject, recipients, email_temp, **kwargs):
    '''
    发送邮件
    :param subject: 主题
    :param recipients: 接收邮箱(列表)
    :param email_temp: 邮件模板
    :param kwargs: 模板参数
    :return:
    '''

    msg = Message(subject=subject, recipients=recipients, sender=current_app.config['MAIL_USERNAME'])
    msg.html = render_template('email/' + email_temp + '.html', **kwargs)

    app = current_app._get_current_object()

    # 多线程
    t = threading.Thread(target=async_send_mail, args=(app, msg))
    t.start()