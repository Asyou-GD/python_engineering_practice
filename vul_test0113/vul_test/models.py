import datetime
import uuid

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from contextlib import contextmanager
from flask_sqlalchemy.query import Query as BaseQuery
from sqlalchemy import Column, String, SmallInteger, BigInteger, Integer, Text
# 加密
from werkzeug.security import generate_password_hash, check_password_hash


class SQLALchemy(_SQLAlchemy):
    """
    数据库回滚数据
    """

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


# user.query.filter_byid(id=id,status=1)
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)


db = SQLALchemy(query_class=Query)


class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer, comment='数据创建时间')
    status = Column(SmallInteger, default=1, comment='数据状态')

    def __init__(self):
        self.create_time = int(datetime.datetime.now().timestamp())

    @property
    def create_datetime(self):
        dt_object = datetime.datetime.fromtimestamp(self.create_time)
        # 使用strftime方法格式化时间
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time

    def delete(self):
        with db.auto_commit():
            self.status = 0
            db.session.add(self)

    def update(self,**kwargs):
        with db.auto_commit():
            for key, value in kwargs.items():
                setattr(self, key, value)
                #hasattr(对象,属性)
                #getattr(对象，属性)(参数)
                #setattr(对象，属性，值)
            db.session.add(self)
# 用户表
class VulUser(Base):
    __tablename__ = 'vul_users'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='用户id')
    user_id = Column(String, nullable=False, comment='用户user_id')
    username = Column(String, nullable=False, comment='用户名')
    password = Column(String, nullable=False, comment='密码')
    auth = Column(SmallInteger, nullable=False, comment='权限')

    @staticmethod
    def insert_user(vul_user: dict):
        vuluser = VulUser()
        with db.auto_commit():
            vuluser.user_id = uuid.uuid4()
            vuluser.username = vul_user.get('username')
            vuluser.password = generate_password_hash(vul_user.get('password'))
            vuluser.auth = vul_user.get('auth')
            db.session.add(vuluser)

    @staticmethod
    def verify(username, password):
        user = VulUser.query.filter_by(username=username).first()  # type:VulUser
        if not user:
            return False

        password_hash = user.password
        if not check_password_hash(password_hash, password):
            return False
        res_data = {}
        if user.auth == 1:
            res_data['scope'] = 'UserScope'
        if user.auth == 2:
            res_data['scope'] = 'AdminScope'
        res_data['uid'] = user.user_id

        return res_data

    @staticmethod
    def add(vul_user: dict):
        with db.auto_commit():
            vulUser = VulUser()
            vulUser.user_id = vul_user.get('user_id')
            vulUser.username = vul_user.get('username')
            vulUser.password = generate_password_hash(vul_user.get('password'))
            vulUser.auth = vul_user.get('auth')
            db.session.add(vulUser)


# 脚本信息表
class VulMsg(Base):
    __tablename__ = 'vul_msg'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='脚本id、主键')
    script_name = Column(String, nullable=False, comment='脚本名')
    vul_point_id = Column(String, nullable=False, comment='漏洞检测点')
    user_id = Column(String, nullable=False, comment='用户id')

    @staticmethod
    def add(vul_msg: dict):
        with db.auto_commit():
            vulMsg = VulMsg()
            vulMsg.script_name = vul_msg.get('script_name')
            vulMsg.vul_point_id = vul_msg.get('vul_point_id')
            vulMsg.user_id = vul_msg.get('user_id')

            vul_point_msgs: list = vul_msg.get('vul_point_msg')
            if vul_point_msgs is not None:
                for vul_point_msg in vul_point_msgs:
                    data = {
                        'serial_num': vul_point_msg.get('serial_num'),
                        'description': vul_point_msg.get('description'),
                        'vul_point_id': vul_msg.get('vul_point_id'),
                        'user_id': vul_msg.get('user_id')
                    }
                    VulPointMsg.add(data)
            db.session.add(vulMsg)

    def to_dict(self):
        return {
            'id': self.id,
            'script_name': self.script_name,
            'vul_point_id': self.vul_point_id,
            'user_id': self.user_id,
            'create_datetime': self.create_datetime,
        }


# 漏洞检测点表
class VulPointMsg(Base):
    __tablename__ = 'vul_point_msg'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='检测点id')
    serial_num = Column(Integer, nullable=False, comment='检测点序号')
    description = Column(Text, nullable=False, comment='检测点说明')
    vul_point_id = Column(String, nullable=False, comment='漏洞检测点id')
    user_id = Column(String, nullable=False, comment='用户id')

    @staticmethod
    def add(vul_point_msg: dict):
        with db.auto_commit():
            vulPointMsg = VulPointMsg()
            vulPointMsg.serial_num = vul_point_msg.get('serial_num')
            vulPointMsg.description = vul_point_msg.get('description')
            vulPointMsg.vul_point_id = vul_point_msg.get('vul_point_id')
            vulPointMsg.user_id = vul_point_msg.get('user_id')
            db.session.add(vulPointMsg)

    def to_dict(self):
        return {
            'id': self.id,
            'serial_num': self.serial_num,
            'description': self.description,
            'vul_point_id': self.vul_point_id,
            'user_id': self.user_id,
            'create_time': self.create_datetime
        }


# 某轮次测试结果记录表
class VulTest(Base):
    __tablename__ = 'vul_test'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='中间表id')
    test_id = Column(String, nullable=False, comment='测试id')
    user_id = Column(String, nullable=False, comment='用户id')
    match_name = Column(String, nullable=False, comment='某轮次IP、PORT信息')

    @staticmethod
    def add(vul_test: dict):
        with db.auto_commit():
            vulTest = VulTest()
            vulTest.test_id = vul_test.get('test_id')
            vulTest.match_name = vul_test.get('match_name')
            vulTest.user_id = vul_test.get('user_id')
            db.session.add(vulTest)

    def to_dict(self):
        return {
            'id': self.id,
            'test_id': self.test_id,
            'user_id': self.user_id,
            'match_name': self.match_name,
            'create_time': self.create_datetime,
        }


# 单脚本测试结果记录表
class VulDetection(Base):
    __tablename__ = 'vul_detection'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    script_name = Column(SmallInteger, nullable=False, comment='脚本名称')
    serial_num = Column(Integer, nullable=False, comment='漏洞点序号')
    description = Column(Text, nullable=False, comment='漏洞描述')
    ip = Column(String(100), nullable=False, comment='IP')
    port = Column(Integer, nullable=False, comment='PORT')
    user_id = Column(String(100), nullable=False, comment='用户id')
    is_alive = Column(SmallInteger, nullable=False, comment='靶机是否可访问')
    is_index_404 = Column(SmallInteger, nullable=False, comment='主页是否404')
    is_vuln = Column(SmallInteger, nullable=False, comment='漏洞是否可利用')
    is_vuln_404 = Column(SmallInteger, nullable=False, comment='漏洞点是否404')
    vul_detection_id = Column(SmallInteger, nullable=False, comment='漏洞检测id')

    @staticmethod
    def add(vul_detection: dict):
        with db.auto_commit():
            vulDetection = VulDetection()
            vulDetection.script_name = vul_detection.get('script_name')
            vulDetection.serial_num = vul_detection.get('serial_num')
            vulDetection.description = vul_detection.get('description')
            vulDetection.ip = vul_detection.get('ip')
            vulDetection.port = vul_detection.get('port')
            vulDetection.user_id = vul_detection.get('user_id')
            vulDetection.is_alive = vul_detection.get('is_alive')
            vulDetection.is_index_404 = vul_detection.get('is_index_404')
            vulDetection.is_vuln = vul_detection.get('is_vlun')
            vulDetection.is_vuln_404 = vul_detection.get('is_vlun_404')
            vulDetection.vul_detection_id = vul_detection.get('vul_detection_id')
            db.session.add(vulDetection)

    @staticmethod
    def add_(vul_detection_list: list):
        for vul_detection in vul_detection_list:
            VulDetection.add(vul_detection)

            data = {
                'vul_detection_id': vul_detection_list[0].get('vul_detection_id'),
                'script_name': vul_detection_list[0].get('script_name')
            }
            VulMsg.add(data)

    def to_dict(self):
        return {
            'id': self.id,
            'vul_detection_id': self.vul_detection_id,
            'script_name': self.script_name,
            'serial_num': self.serial_num,
            'description': self.description,
            'is_alive': self.is_alive,
            'is_index_404': self.is_index_404,
            'is_vuln': self.is_vuln,
            'is_vuln_404': self.is_vuln_404,
            'ip': self.ip,
            'port': self.port,
            'user_id': self.user_id,
            'create_datetime': self.create_datetime,
        }


# 单脚本测试记录表
class VulSingleTest(Base):
    __tablename__ = 'vul_single_test'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    vul_detection_id = Column(String(100), nullable=False, comment='测试结果id')
    script_name = Column(String(255), nullable=False, comment='脚本名')
    user_id = Column(String(100), nullable=False, comment='用户id')

    @staticmethod
    def add(vul_single_test: dict):
        with db.auto_commit():
            vulSingleTest = VulSingleTest()
            vulSingleTest.vul_detection_id = vul_single_test.get('vul_detection_id')
            vulSingleTest.script_name = vul_single_test.get('script_name')
            vulSingleTest.user_id = vul_single_test.get('user_id')
            db.session.add(vulSingleTest)

    def to_dict(self):
        return {
            'id': self.id,
            'vul_detection_id': self.vul_detection_id,
            'script_name': self.script_name,
            'user_id': self.user_id,
            'create_time': self.create_datetime,
        }


# 某轮次测试详细结果表
class VulDetectionAll(Base):
    __tablename__ = 'vul_detection_all'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    match_name = Column(String, nullable=False, comment='轮次名称')
    match_id = Column(String, nullable=False, comment='轮次id')
    team_name = Column(Integer, nullable=False, comment='队伍名称')
    script_name = Column(SmallInteger, nullable=False, comment='脚本名称')
    serial_num = Column(Integer, nullable=False, comment='漏洞点序号')
    description = Column(Text, nullable=False, comment='漏洞描述')
    ip = Column(String, nullable=False, comment='IP')
    port = Column(Integer, nullable=False, comment='PORT')
    user_id = Column(String, nullable=False, comment='用户id')
    is_alive = Column(SmallInteger, nullable=False, comment='靶机是否可访问')
    is_index_404 = Column(SmallInteger, nullable=False, comment='主页是否404')
    is_vuln = Column(SmallInteger, nullable=False, comment='漏洞是否可利用')
    is_vuln_404 = Column(SmallInteger, nullable=False, comment='漏洞点是否404')
    test_id = Column(SmallInteger, nullable=False, comment='轮次ID')

    @staticmethod
    def add(vul_detection_all: dict):
        with db.auto_commit():
            vulDetectionAll = VulDetectionAll()
            vulDetectionAll.match_name = vul_detection_all.get('match_name')
            vulDetectionAll.match_id = vul_detection_all.get('match_id')
            vulDetectionAll.team_name = vul_detection_all.get('team_name')
            vulDetectionAll.script_name = vul_detection_all.get('script_name')
            vulDetectionAll.serial_num = vul_detection_all.get('serial_num')
            vulDetectionAll.description = vul_detection_all.get('description')
            vulDetectionAll.ip = vul_detection_all.get('ip')
            vulDetectionAll.port = vul_detection_all.get('port')
            vulDetectionAll.user_id = vul_detection_all.get('user_id')
            vulDetectionAll.is_alive = vul_detection_all.get('is_alive')
            vulDetectionAll.is_index_404 = vul_detection_all.get('is_index_404')
            vulDetectionAll.is_vuln = vul_detection_all.get('is_vuln')
            vulDetectionAll.is_vuln_404 = vul_detection_all.get('is_vuln_404')
            vulDetectionAll.test_id = vul_detection_all.get('test_id')
            db.session.add(vulDetectionAll)


# 某轮次测试 IP 信息表
class VulIP(Base):
    __tablename__ = 'vul_ip'
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    match_name = Column(String, nullable=False, comment='轮次名称')
    match_id = Column(String, nullable=False, comment='轮次id')
    team_name = Column(Integer, nullable=False, comment='队伍名称')
    script_name = Column(SmallInteger, nullable=False, comment='脚本名称')
    serial_num = Column(Integer, nullable=False, comment='漏洞点序号')
    ip = Column(String, nullable=False, comment='IP')
    port = Column(Integer, nullable=False, comment='PORT')
    user_id = Column(String, nullable=False, comment='用户id')

    @staticmethod
    def add(vul_ip: dict):
        with db.auto_commit():
            vulIp = VulIP()
            vulIp.team_name = vul_ip['team_name']
            vulIp.script_name = vul_ip['script_name']
            vulIp.serial_num = vul_ip.get('serial_num')
            vulIp.ip = vul_ip.get('ip')
            vulIp.port = vul_ip.get('port')
            vulIp.match_name = vul_ip.get('match_name')
            vulIp.match_id = vul_ip.get('match_id')
            vulIp.user_id = vul_ip.get('user_id')
            db.session.add(vulIp)
            return vulIp
