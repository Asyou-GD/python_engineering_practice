import datetime
import uuid

from authlib.jose import jwt
#token里面存什么#
#-------------- uid  用户的id
#-------------- scope 权限
#-------------- exp token有时效时间


import config
def generate_token(uid, scope, app, expiration_time = 60*2):
    headers = {'alg': 'HS256'}
    exp = datetime.datetime.now() + datetime.timedelta(minutes=expiration_time)
    pyload = {
        'uid':uid,
        'scope':scope,
        'exp':exp
    }
    t = jwt.encode(headers,pyload,app.config.get('SECRET_KEY'))
    # t = jwt.encode(headers, pyload, config.Baseconfig.SECRET_KEY)
    return t


def generate_token_with_key(uid, scope, expiration_time=60 * 2):
    """

    :param uid:
    :param scope:
    :param expiration_time:
    :return:
    """
    key = b"\xc7i9\x8f7\xfe!\xa0\x96F\x1e\xcc\xdf\xd1o\r'\xaf\xfe5\xbf`\x0b\xad\x10\x83\xd2\x7f\xe0\xcc\r\xf8"
    headers = {'alg': 'HS256'}
    exp = datetime.datetime.now() + datetime.timedelta(minutes=expiration_time)
    pyload = {
        'uid': uid,
        'scope': scope,
        'exp': exp
    }
    t = jwt.encode(headers, pyload, key)
    # t = jwt.encode(headers, pyload, config.Baseconfig.SECRET_KEY)
    return t