

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
    print(token,'token')
    user = verify_token(token)
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
    import requests
    from flask import Flask, jsonify
    from flask_httpauth import HTTPBasicAuth

    app = Flask(__name__)
    auth = HTTPBasicAuth()


    @auth.verify_password
    def verify_password(username, password):
        return username == 'admin' and password == 'secret'


    @app.route('/')
    @auth.login_required
    def index():
        return jsonify({"message": "Hello, {}!".format(auth.current_user())})


    if __name__ == "__main__":
        app.run(debug=True)

    # 目标 URL
    url = 'http://127.0.0.1:5000/'

    # 用户名和密码
    username = 'admin'
    password = 'secret'

    # 发送 GET 请求并提供基本认证凭证
    response = requests.get(url, auth=(username, password))

    # 打印响应内容
    print(response.text)
