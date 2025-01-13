#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-10 16:15
# @Author  : skilywen

#验证token是否失效
#token如何传入服务端 ：1. 在提交的json数据中增加token字段 2. 在headers中增加token字段 3. basic-auth headers中增减一个authoriation字段，token的base64编码
from flask_httpauth import HTTPBasicAuth
from authlib.jose import jwt
from flask import current_app, g

from libs.error_code import AuthFailed
from collections import namedtuple
from flask import request

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'scope'])

@auth.verify_password
def verify_password(token, password):
    user = verify_token(token)
    if user:
        g.uid = user.uid
        return True

def verify_token(token):
    """
    验证token是否失效
    :param token:
    :return:
    """
    try:
        data = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        data.validate()
    except:
        raise AuthFailed('令牌失效')

    uid = data.get('uid')
    scope = data.get('scope')
    return User(uid, scope)




