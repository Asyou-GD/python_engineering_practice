import importlib
import json
import re
import html
import uuid
from flask import Flask, request, g, render_template, redirect, jsonify
from werkzeug.exceptions import Unauthorized
from Libs.error_code import AuthFailed

import Libs.token_auth
from config import db_config, verify
from models import *
from Libs import tools, error_code, tokens
from Libs.token_auth import auth
from Libs import token_auth
from Libs.error_code import ParametersException
import pandas as pd
from validators.forms import SingleDetailForm, WebStartForm, StartScriptForm
import flask_caching
from validators import forms

app = Flask(__name__)
verify(cofig=db_config['development'])
app.config.from_object(db_config['development'])
db.init_app(app)

cache = flask_caching.Cache(config={'CACHE_TYPE': 'simple'})
cache.init_app(app)

with open('conf.json', 'r') as f:
    login_data = json.load(f)

with app.app_context():
    db.create_all()  # 创建所有表


@app.cli.command('creat_admin')
def insert_admin():
    pass


@app.route('/verify/web/add', methods=['POST'])
@auth.login_required
def wed_add():
    """
    加数据验证
    :return:
    """
    data_json = html.escape(request.data.decode(), quote=False)
    data = json.loads(data_json)
    script_name = data.get('script_name')
    vul_point_msg = data.get('vul_point_msg')
    if not script_name or not vul_point_msg:
        raise ParametersException()
    if not re.match(r'^\w+$', script_name):
        raise ParametersException()
    vulMsg = VulMsg.query.filter_by(script_name=script_name, user_id=g.uid).first()
    if vulMsg:
        raise ParametersException(msg='脚本已经存在，添加失败')
    for vulpoint in vul_point_msg:
        serial_num = vulpoint.get('serial_num')
        if not isinstance(serial_num, int):
            raise ParametersException()
    data['vul_point_id'] = uuid.uuid4()
    data['user_id'] = g.uid
    VulMsg.add(data)
    return {'code':200, 'status':1, 'msg':'操作成功'}


@app.route('/verify/web/start/<id>', methods=['POST'])
@auth.login_required
def web_start(id):
    """
    改写表单验证
    :param id:
    :return:
    """
    # data = request.json
    # ip = data.get('ip')
    # port = data.get('port')
    webStartForm = WebStartForm().validate_for_api()
    data = webStartForm.data
    ip = data.get('ip')
    port = data.get('port')

    #检测id所对应的脚本信息是否存在
    vulMsg = VulMsg.query.filter_by(id=id).first()
    if vulMsg is None:
        return {'code':200, 'status':0, 'msg':'参数有误'}

    #检测数据库中记录的脚本信息在scripts目录下是否存在
    #读取scripts目录下所有的python脚本，放入列表中
    sn_lst = tools.get_all_scripts(app)
    script_name = vulMsg.script_name
    if script_name not in sn_lst:
        return {'code':200, 'status':0, 'msg':f'{script_name}脚本不存在'}
    func = importlib.import_module(app.config.get('SCRIPTS_PATH') + script_name)
    url = tools.generate_url(ip, port)
    vul_point_id = vulMsg.vul_point_id
    vulPointMsgs = VulPointMsg.query.filter_by(vul_point_id=vul_point_id).all()
    vul_detection_id = uuid.uuid4()
    result = []
    if hasattr(func, app.config.get('FUNCTION_NAME')):
        for vulPointMsg in vulPointMsgs:
            serial_num = vulPointMsg.serial_num
            numTuple = tools.bool_to_num(getattr(func, app.config.get('FUNCTION_NAME'))(url, str(serial_num)))
            data = {
                    'vul_detection_id':vul_detection_id,
                    'script_name':script_name,
                    'serial_num':serial_num,
                    'is_alive':numTuple.is_alive,
                    'is_index_404':numTuple.is_index_404,
                    'is_vuln':numTuple.is_vuln,
                    'is_vuln_404':numTuple.is_vuln_404,
                    'ip':ip,
                    'port':port,
                    'description':vulPointMsg.description,
                    'user_id':g.uid
            }
            result.append(data)
        VulDetection.add_(result)
        print('result',result)
        print('vulPointMsgs',vulPointMsgs)
        return {'code':200, 'status':1, 'msg':'操作成功', 'data':result}
    else:
        return {'code': 200, 'status': 0, 'msg': '脚本调用失败'}


@app.route('/ip/upload', methods=['POST'])
@auth.login_required
def upload_ip():
    """
    数据验证
    :return:
    """
    file = request.files['file']
    match_name = request.form.get('match_name')
    if not file or not match_name:
        raise ParametersException()
    if re.search(r'[<>]', match_name):
        raise ParametersException()
    matchName = VulIP.query.filter_by(match_name=match_name, user_id=g.uid).first()
    if matchName:
        return {'code':200, 'status':0, 'msg':'轮次名称重复'}
    match_id = uuid.uuid4()
    if file:
        ext = tools.allowed_file(file.filename, app.config.get('EXTS'))
        if ext is None:
            return {'code':200, 'status':0, 'msg':'文件类型有误'}
        df = pd.read_excel(file)
        success = 0
        failed = 0
        for index, row in df.iterrows():
            data = {
                'team_name':row['队伍名'],
                'script_name':row['脚本名'],
                'serial_num':row['漏洞点'],
                'ip' :row['IP'],
                'port':row['PORT'],
                'match_id':match_id,
                'match_name':match_name,
                'user_id':g.uid
            }
            if VulIP.add(data):
                success += 1
            else:
                failed += 1
        return {'code':200, 'success_count':success, 'failed_count':failed, 'status':1}
    else:
        return {'code': 200, 'status': 0, 'msg': '上传出错'}


@app.route('/web/start/all', methods=['POST'])
@auth.login_required
def web_start_all():
    """
    表单验证
    :return:
    """
    # data = request.json
    # match_name = data.get('match_name')
    startScriptForms = StartScriptForm().validate_for_api()
    data = startScriptForms.data
    match_name = data.get('match_name')
    vulIps = VulIP.query.filter_by(match_name=match_name, user_id=g.uid).all()
    if vulIps is None:
        return {'code':200, 'status':1, 'msg':'参数有误vulIps为空'}

    filenames = tools.get_all_scripts(app)
    script_names = set([vulIp.script_name for vulIp in vulIps])
    print('filenames',filenames)
    print('script_names',script_names)
    if not ( set(filenames) & script_names  == script_names):
        return {'code':200, 'status':1, 'msg':'参数有误'}
    test_id = uuid.uuid4()
    result = []
    for vulIp in vulIps:
        vulMsg = VulMsg.query.filter_by(script_name=vulIp.script_name,user_id=g.uid).first()
        vul_point_id = vulMsg.vul_point_id
        ip = vulIp.ip
        port = vulIp.port
        url = tools.generate_url(ip, port)
        script_name = vulIp.script_name
        serial_num = vulIp.serial_num
        vulPointMsg = VulPointMsg.query.filter_by(vul_point_id=vul_point_id, serial_num=serial_num).first()
        if vulPointMsg is None:
            return {'code':200, 'status':1, 'msg':'参数有误'}
        func = importlib.import_module(app.config.get('SCRIPTS_PATH') + script_name)
        if hasattr(func, app.config.get('FUNCTION_NAME')):
            numTuple = tools.bool_to_num(getattr(func, app.config.get('FUNCTION_NAME'))(url, str(serial_num)))
            data = {
                    'script_name': script_name,
                    'serial_num': serial_num,
                    'is_alive': numTuple.is_alive,
                    'is_index_404': numTuple.is_index_404,
                    'is_vuln': numTuple.is_vuln,
                    'is_vuln_404':numTuple.is_vuln_404,
                    'description': vulPointMsg.description,
                    'ip': ip,
                    'port': port,
                    'match_name':vulIp.match_name,
                    'match_id':vulIp.match_id,
                    'test_id':test_id,
                    'team_name':vulIp.team_name,
                    'user_id':g.uid
                }
            VulDetectionAll.add(data)
            result.append(data)
    else:
        VulTest.add({'match_name':match_name, 'test_id':test_id, 'user_id':g.uid})
        return {'code':200, 'status':1, 'data':result}


@app.route('/detection/single/detail', methods=['POST'])
@auth.login_required
def get_single_detail():
    # data = request.json
    # vul_detection_id = data.get('vul_detection_id')
    form = SingleDetailForm().validate_for_api()
    vul_detection_id = form.data.get('vul_detection_id')
    vulDetections = VulDetection.query.filter_by(vul_detection_id=vul_detection_id, user_id=g.uid).all()
    result = []
    if vulDetections:
        for vulDetection in vulDetections:
            result.append(vulDetection.to_dict())
    return {'code':200, 'status':1, 'msg':'', 'data':result}


@app.route('/imagecode')
def get_image_code():
    image_code = tools.generate_image_code()
    uid = str(uuid.uuid1())

    # 将验证码存储到缓存中
    cache.set(uid, image_code, timeout=300)  # 缓存 5 分钟（300 秒）
    _ = """
    cache.set()
        这是 flask_caching 的核心方法，用于将数据存储到缓存中。
        格式：cache.set(key, value, timeout=TTL)
    key：缓存的键名（如 uid）。
    value：要缓存的值（如 image_code）。
    timeout：可选参数，指定缓存的超时时间，单位是秒。
    缓存配置
        CACHE_TYPE: 'simple' 使用简单的内存缓存，适用于开发环境。如果是生产环境，
        可以切换到 Redis、Memcached 等更高效的缓存。
    """
    return {
        'uid': uid,
        'image_code': image_code,
    }


@app.route('/get_image_code/<uid>', methods=['GET'])
def image_code(uid):
    return cache.get(uid) or '失败'


@app.route('/token', methods=['POST'])
def get_token():
    form = forms.UserForm().validate_for_api()
    username = form.username.data
    password = form.password.data
    image_code = form.image_code.data
    uid = form.uid.data

    code = cache.get(uid)
    if code is None:
        raise error_code.AuthFailed(msg='图形验证码验证失败--')

    if image_code.lower() != code.lower():
        raise error_code.AuthFailed(msg='图形验证码验证失败')

    user = VulUser.verify(username, password)
    if not user:
        raise error_code.AuthFailed(msg='用户名或者密码错误')

    token = tokens.generate_token(user.get('uid'), user.get('scope'), app).decode()
    t = {
        'status': 1,
        'code': 200,
        'token': token
    }
    login_data['login_state'] = 1
    login_data['user_name'] = username
    with open('conf.json', 'w') as f:
        json.dump(login_data, f)
    return t

@app.route('/register', methods=['POST'])
def register():
    form = forms.UserForm().validate_for_api()
    username = form.username.data
    password = form.password.data
    image_code = form.image_code.data
    uid = form.uid.data

    code = cache.get(uid)
    if code is None:
        raise error_code.AuthFailed(msg='图形验证码验证失败--')

    if image_code.lower() != code.lower():
        raise error_code.AuthFailed(msg='图形验证码验证失败')
    VulUser.insert_user(request.json)
    return {'code': 200, 'status': 1, 'msg': '注册成功'}

@app.route('/verify/web/list')
@auth.login_required
def web_list():
    """
    获取当前所有的脚本信息。
    :return:
    """
    user_id = g.uid
    print(g.uid,'g.uid')
    vulMsgs = VulMsg.query.filter_by(user_id=user_id).all()
    result = []
    if vulMsgs:
        for vulMsg in vulMsgs:
            vul_point_id = vulMsg.vul_point_id
            vul_point_msgs = VulPointMsg.query.filter_by(vul_point_id=vul_point_id).all()
            data = vulMsg.to_dict()
            data['scripts'] = [vul_point_msg.to_dict() for vul_point_msg in vul_point_msgs]
            result.append(data)
        # data['code']=200
        # data['status'] = 1
        data = tools.success({'data':result})
    else:
        data = {'code':200, 'status':0, 'msg':'没有任何脚本信息', }
    return data


@app.route('/detection/all/list')
@auth.login_required
def detection_all():
    user_id = g.uid
    vul_tests = VulTest.query.filter_by(user_id=user_id).all()
    result = []
    if vul_tests:
        for vul_test in vul_tests:
            result.append(vul_test.to_dict())
    return tools.success({'data':result})


@app.route('/detection/all/detail', methods=['POST'])
@auth.login_required
def detection_all_lst():
    """
    接口：查询某一轮次测试的具体信息
    功能：根据测试 ID，获取某轮次测试的详细信息，并返回结果。
    """
    # 获取并验证请求数据
    detectionForm = forms.DetectionForm().validate_for_api()
    data = detectionForm.data
    test_id = data.get('test_id')

    # 根据测试 ID 查询详细数据
    vul_detection_all = VulDetectionAll.query.filter_by(test_id=test_id).all()
    result = []
    if vul_detection_all:
        for vul_detection in vul_detection_all:
            result.append(vul_detection.to_dict())
    return tools.success({'data': result})


@app.route('/detection/single/list')
@auth.login_required
def get_single_test():
    """
    接口：获取所有单次检测的结果记录
    功能：根据用户 ID，获取所有单次检测结果的记录，并返回结果。
    """
    user_id = g.uid
    print(g.uid)
    vulSingleTests = VulSingleTest.query.filter_by(user_id=user_id).all()
    result = []
    if vulSingleTests:
        for vulSingleTest in vulSingleTests:
            result.append(vulSingleTest.to_dict())
    return tools.success({'data': result})



@app.route('/verify/matchnames')
@auth.login_required
def get_match_name():
    vulIps = VulIP.query.filter_by(user_id=g.uid).all()
    if vulIps:
        match_name = [vulIp.match_name for vulIp in vulIps]
        match_name = list(set(match_name))
        return tools.success({'data':match_name})
    raise ParametersException()

@app.route('/creat_user',methods =['POST'])
def creat_user():
    data = request.form.to_dict()
    if len(data) == 0:
        data = request.json
    VulUser.insert_user(data)
    return tools.success({},msg='创建成功')

@app.route('/')
def hello_world():  # put application's code here
    return redirect('login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/exit')
def exit():
    login_data['login_state'] = 0
    with open('conf.json', 'w') as f:
        json.dump(login_data, f)
    return redirect('login')    

@app.route('/scriptshow')
def scriptshow():
    if login_data['login_state'] == 1:
        print(login_data)
        return render_template('scriptshow.html',config = login_data)
    token = request.args.get('token')
    return handle_auth(token = token, template='scriptshow.html')
    

@app.route('/iplist')
def iplist():
    if login_data['login_state'] == 1:
        return render_template('iplist.html')
    return handle_auth_failed('')

@app.route('/batch-detail')
def batch_detail():
    if login_data['login_state'] == 1:
        return render_template('batch-detail.html')
    return handle_auth_failed('')


@app.route('/batchall')
def batchall():
    if login_data['login_state'] == 1:
        return render_template('batchall.html')
    return handle_auth_failed('')

@app.route('/open-detection')
def open_detection():
    if login_data['login_state'] == 1:
        return render_template('open-detection.html')
    return handle_auth_failed('')

@app.route('/run')
def run():
    if login_data['login_state'] == 1:
        return render_template('run.html')
    return handle_auth_failed('')

@app.route('/single')
def single():
    if login_data['login_state'] == 1:
        return render_template('single.html')
    return handle_auth_failed('')

@app.route('/single-detail')
def single_detail():
    if login_data['login_state'] == 1:
        return render_template('single-detail.html')
    return handle_auth_failed('')

@app.route('/verify/web/delete/<id>')
@auth.login_required
def web_delete(id):
    vulMsg = VulMsg.query.filter_by(id=id, user_id=g.uid).first()
    if vulMsg is None:
        raise ParametersException()
    vul_point_id = vulMsg.vul_point_id
    vulPointMsgs = VulPointMsg.query.filter_by(vul_point_id=vul_point_id).all()
    for vulPointMsg in vulPointMsgs:
        # vulPointMsg.delete()
        vulPointMsg.update(status=0)
    # vulMsg.delete()
    vulMsg.update(status=0)
    return {'code':200, 'status':1, 'msg':'删除成功'}

@app.route('/error')
# 添加全局错误处理器
def handle_auth_failed(e):
    error_data = {
        'code': 401,
        'status': 0,
        'msg':'令牌失效',
        'error_code': 1001,
        'request': request.method + ' ' + request.path
    }
    return render_template('error.html', 
                         error_json=json.dumps(error_data, indent=4, ensure_ascii=False)), 401

def handle_auth(token,template):
    global login_data
    try:
        if token_auth.verify_token(token):
            login_data['login_state'] = 1
            with open('conf.json', 'w') as f:
                json.dump(login_data, f)
            return render_template(template,config = login_data)
        login_data['login_state'] = 0
        return handle_auth_failed('')
    except Exception as e:
        login_data['login_state'] = 0
        return handle_auth_failed(e)
    

@app.route('/get_vul_msg')
@auth.login_required
def get_vul_msg():
    vulMsgs = VulMsg.query.filter_by(user_id=g.uid).all()
    result = []
    if vulMsgs:
        for vulMsg in vulMsgs:
            result.append({
                'id': vulMsg.id,
                'script_name': vulMsg.script_name
            })
        print("查询到的数据:", result)  # 添加调试信息
        return tools.success({'data': result})
    print("没有查询到数据, user_id:", g.uid)  # 添加调试信息
    return {'code': 200, 'status': 0, 'msg': '没有数据'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)


