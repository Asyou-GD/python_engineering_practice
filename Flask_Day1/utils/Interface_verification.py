import json

import requests
import Libs.token_auth
import Libs.tokens
import config
from models import *

Base_url = 'http://127.0.0.1/'


def web_add():
    url = 'http://127.0.0.1:5000/verify/web/add'
    json = {
        "script_name": "abc",
        "vul_point_msg": [
            {
                "serial_num": 1,
                "description": "第一处：/search  命令执行"
            },
            {
                "serial_num": 2,
                "description": "第二处：/upload  yaml反序列漏洞"
            }
        ]
    }
    res = requests.post(url, json=json).json()
    # res['msg'] = res['msg'].encode('utf8').decode('utf8')
    print(res)


def web_start(id):
    url = f'http://127.0.0.1:5000/verify/web/start/{id}'
    data = {
        'ip': '4.2.31.2',
        'port': '80',
    }
    res = requests.post(url, json=data).json()
    res = json.dumps(eval(res.encode().decode('utf8')), ensure_ascii=False, indent=2)
    print(res)


def upload_ip(token):
    url = Base_url + 'ip/upload'
    with open('../IP1.xlsx', 'rb') as f:
        # 上传文件
        files = {'file': f}
        data = {'match_name': '测试而已'}
        headers = {'Authorization': f'token {token}'}
        response = requests.post(url, files=files, data=data, headers=headers).text
    print(response)


def get_image_code():
    url = Base_url + 'imagecode'
    res = requests.get(url).json()
    print(res)
    print('GET IMAGE_CODE')
    res_ = requests.get(Base_url + f'get_image_code/{res["uid"]}')
    print(res_.text)
    return res


def get_tokens(image_code=None, uid=None):
    url = Base_url + 'token'
    data = {
        "username": "test_user",
        "password": "123456",
        "image_code": "CEb8",
        "uid": "b3a3a923-cf4b-11ef-b005-c8cb9e65315f",
    }
    if image_code is not None:
        data['image_code'] = image_code
        data['uid'] = uid
    res = requests.post(url, json=data).json()

    return  res


def test_tokens():
    from authlib.jose import jwt

    # 生成一个测试 Token
    SECRET_KEY = "\xc7i9\x8f7\xfe!\xa0\x96F\x1e\xcc\xdf\xd1o\r'\xaf\xfe5\xbf`\x0b\xad\x10\x83\xd2\x7f\xe0\xcc\r\xf8"

    payload = {
        "uid": "12345",
        "scope": "admin"
    }

    token = jwt.encode({'alg': 'HS256'}, payload, SECRET_KEY)

    data = jwt.decode(token, SECRET_KEY)
    print(data, data.validate())

def test():
    #
    #
    # res = get_image_code()
    # token = get_tokens(res['image_code'], res['uid'])

    upload_ip(
        token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1aWQiOiI1YTk3NDRlMy02YTQ4LTQxZDYtYWMxYi05M2UzNTAyNmNjYjEiLCJzY29wZSI6IlVzZXJTY29wZSIsImV4cCI6MTczNjU1MDQ2NH0.7mCBk3vHM4rn4ZoNy3KmuI4mMmcfujsvBJWDBcg8qFs')
    from authlib.jose import jwt
    # from flask import current_app
    # print(current_app.config.get('SECRET_KEY'))
    # # print(jwt.decode(token, current_app.config.get('SECRET_KEY')))

    # token = Libs.tokens.generate_token_with_key('5a9744e3-6a48-41d6-ac1b-93e35026ccb1','UserScope').decode()
    # print(token)
    # data = jwt.decode(token, key=config.Baseconfig.SECRET_KEY)
    # print(data)

def creat_user():
    url = Base_url + 'creat_user'
    vul_user = {
        'username':'lzl',
        'password':'GD0818109',
        'auth':1
    }
    res = requests.post(url, data=vul_user).text
    print(res)
creat_user()