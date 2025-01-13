#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2025-01-07 16:53
# @Author  : skilywen
import os
from collections import namedtuple
import string
import random
from werkzeug.exceptions import HTTPException

from libs.error import APIException
from libs.error_code import ServerException


def get_all_scripts(app):
    """
    获取scripts目录下所有python脚本名称
    :return:
    """
    abs_path = app.config.get('SCRIPTS_ABS_PATH')
    filenames = os.listdir(abs_path)
    sn_lst = []
    for filename in filenames:
        if filename.endswith('.py'):
            file, ext = filename.split('.')
            sn_lst.append(file)
    return sn_lst

def generate_url(ip, port:int):
    return 'http://' + ip + ':' + str(port)


def bool_to_num(bool_lst:list):
    NumTuple = namedtuple('NumTuple', ['is_alive', 'is_index_404', 'is_vuln', 'is_vuln_404', 'description'])
    is_alive = 1 if bool_lst[0] else 0
    is_index_404 = 1 if bool_lst[1] else 0
    is_vuln = 1 if bool_lst[2] else 0
    is_vuln_404= 1 if bool_lst[3] else 0
    description = bool_lst[4]
    return NumTuple(is_alive, is_index_404, is_vuln, is_vuln_404, description)

def allowed_file(filename, ext_allowed):
    if '.' in filename:
        ext = filename.split('.')[-1].lower()
        if ext in ext_allowed:
            return ext

def generate_image_code():
    """
    生成4位图形验证码
    :return:
    """
    code_str = string.ascii_letters + string.digits
    s = ''
    for i in range(4):
        s += code_str[random.randint(0, len(code_str)-1)]
    return s


def success(dic, code=200, status=1, msg=''):
    dic['code'] = code
    dic['status'] = status
    dic['msg'] = msg
    return dic








