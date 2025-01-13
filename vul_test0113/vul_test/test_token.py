#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-10 09:07
# @Author  : skilywen
from authlib.jose import jwt

payload = {
    'username':'tom'
}
header = {'alg':'HS256'}
token = jwt.encode(header, payload, '123456')
print(token)
