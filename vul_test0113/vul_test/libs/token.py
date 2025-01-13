#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-10 15:22
# @Author  : skilywen

#token里面存什么？
#uid   用户ID
#scope 权限
#exp   token有时效

from authlib.jose import jwt
from datetime import datetime, timedelta

def generate_token(uid, scope, app, expiration_time=60*2):
    header = {'alg':'HS256'}
    exp = datetime.now() + timedelta(minutes=expiration_time)
    payload = {
                'uid':uid,
                'scope':scope,
                'exp':exp
    }
    t = jwt.encode(header, payload, app.config.get('SECRET_KEY'))
    return t


