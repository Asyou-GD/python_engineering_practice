#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-09 16:20
# @Author  : skilywen
from libs.error import APIException

class ParametersException(APIException):
    status = 0
    msg = '参数错误'
    code = 400
    error_code = 1000

class AuthFailed(APIException):
    status = 0
    msg = '验证失败'
    code = 401
    error_code = 1001


class ServerException(APIException):
    status = 0
    msg = '验证失败'
    code = 500
    error_code = 1001