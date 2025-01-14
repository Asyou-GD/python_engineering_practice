

#验证token是否失效
#token如何传入服务器端
"""
1. 在headers增加token字段
2. 在传入的json数据中加入tokens字段
3。 basic-auth: 在headers中增加token的base64编码，Authorization
"""
from flask_httpauth import HTTPBasicAuth,HTTPTokenAuth
from authlib.jose import jwt
from flask import current_app, g
from Libs.error_code import AuthFailed
from collections import namedtuple

auth = HTTPTokenAuth(scheme='Token')
User = namedtuple('User', ['uid','scope'])


@auth.verify_token
def verify_password(token):
    user = verify_token(token)
    print(user,'user')
    if user:
        g.uid = user.uid
        return True
    return False

def verify_token(token):
    """
    验证token是否失效
    :param token:
    :return:
    """
    try:
        data = jwt.decode(token, current_app.config.get('SECRET_KEY'))
        data.validate()
    except Exception as e:
        print(e)
        raise AuthFailed('令牌失效')
    uid = data.get('uid')
    scope = data.get('scope')
    return User(uid, scope)

if __name__ == '__main__':
    print(1)