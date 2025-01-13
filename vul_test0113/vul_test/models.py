import uuid
from contextlib import contextmanager

from flask_sqlalchemy import SQLAlchemy as _SQLAlchemy
from flask_sqlalchemy import BaseQuery
from sqlalchemy import Column, String, SmallInteger, Integer, Text
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

#db.session.add(user)  db.session.commit()
class SQLAlchemy(_SQLAlchemy):
    """
    数据库回滚机制
    """

    @contextmanager
    def auto_commit(self):
        try:
            yield
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

#User.query.filter_by(id=id, status=1)
class Query(BaseQuery):
    def filter_by(self, **kwargs):
        if 'status' not in kwargs.keys():
            kwargs['status'] = 1
        return super(Query, self).filter_by(**kwargs)
db = SQLAlchemy(query_class=Query)

class Base(db.Model):
    __abstract__ = True
    create_time = Column(Integer)
    status = Column(SmallInteger, default=1)

    def __init__(self):
        self.create_time = int(datetime.now().timestamp())

    @property
    def create_datetime(self):
        dt_object = datetime.fromtimestamp(self.create_time)
        # 使用strftime方法格式化时间
        formatted_time = dt_object.strftime('%Y-%m-%d %H:%M:%S')
        return formatted_time

    def delete(self):
        with db.auto_commit():
            self.status = 0
            db.session.add(self)

    def update(self, **kwargs):
        with db.auto_commit():
            for k, v in kwargs.items():
                #k=> 'id'  self.id = v
                setattr(self, k, v)
            db.session.add(self)


class VulMsg(Base):
    __tablename__ = 'vul_msg'
    id = Column(Integer, primary_key=True)
    script_name = Column(String)
    vul_point_id = Column(String)
    user_id = Column(String)

    def to_dict(self):
        return {'id':self.id, 'script_name':self.script_name, 'create_time':self.create_datetime}




    @staticmethod
    def add(vul_msg:dict):
        with db.auto_commit():
            vulMsg = VulMsg()
            vulMsg.script_name = vul_msg.get('script_name')
            vulMsg.vul_point_id = vul_msg.get('vul_point_id')
            vulMsg.user_id = vul_msg.get('user_id')
            vul_point_msgs = vul_msg.get('vul_point_msg')
            for vul_point_msg in vul_point_msgs:
                data = {
                        'serial_num':vul_point_msg.get('serial_num'),
                        'description':vul_point_msg.get('description'),
                        'vul_point_id':vul_msg.get('vul_point_id'),
                        'user_id':vul_msg.get('user_id'),
                }
                VulPointMsg.add(data)
            db.session.add(vulMsg)

class VulPointMsg(Base):
    __tablename__ = 'vul_point_msg'
    id = Column(Integer, primary_key=True)
    serial_num = Column(Integer)
    description = Column(Text)
    vul_point_id = Column(String)
    user_id = Column(String)

    def to_dict(self):
        return {'serial_num':self.serial_num, 'description':self.description}

    @staticmethod
    def add(vul_point_msg:dict):
        with db.auto_commit():
            vulPointMsg = VulPointMsg()
            vulPointMsg.serial_num = vul_point_msg.get('serial_num')
            vulPointMsg.description = vul_point_msg.get('description')
            vulPointMsg.vul_point_id = vul_point_msg.get('vul_point_id')
            vulPointMsg.user_id = vul_point_msg.get('user_id')
            db.session.add(vulPointMsg)


class VulSingleTest(Base):
    __tablename__ = 'vul_single_test'
    id = Column(Integer, primary_key=True)
    vul_detection_id = Column(String)
    script_name = Column(String)
    user_id = Column(String)

    def to_dict(self):
        return {
            'vul_detection_id':self.vul_detection_id,
            'script_name':self.script_name,
            'create_datetime':self.create_datetime
        }

    @staticmethod
    def add(vul_single_test:dict):
        with db.auto_commit():
            vulSingleTest =VulSingleTest()
            vulSingleTest.vul_detection_id = vul_single_test.get('vul_detection_id')
            vulSingleTest.script_name = vul_single_test.get('script_name')
            vulSingleTest.user_id = vul_single_test.get('user_id')
            db.session.add(vulSingleTest)

class VulDetection(Base):
    __tablename__ = 'vul_detection'
    id = Column(Integer, primary_key=True)
    vul_detection_id = Column(String)
    script_name = Column(String)
    user_id = Column(String)
    serial_num = Column(Integer)
    is_alive = Column(SmallInteger)
    is_index_404 = Column(SmallInteger)
    is_vuln = Column(SmallInteger)
    is_vuln_404 = Column(SmallInteger)
    ip = Column(String)
    port = Column(Integer)
    description = Column(Text)


    # def update(self, scrip_name, ip, port):
    #     with db.auto_commit():
    #         self.script_name = scrip_name
    #         self.ip = ip
    #         self.port = port
    #         db.session.add(self)

    def to_dict(self):
        return {
                'id':self.id,
                'vul_detection_id':self.vul_detection_id,
                'script_name':self.script_name,
                'serial_num':self.serial_num,
                'is_alive':self.is_alive,
                'is_index_404':self.is_index_404,
                'is_vuln':self.is_vuln,
                'is_vuln_404':self.is_vuln_404,
                'ip':self.ip,
                'port':self.port,
                'description':self.description,
                'create_datetime':self.create_datetime,
        }


    @staticmethod
    def add(vul_detection:dict):
        with db.auto_commit():
            vulDetection = VulDetection()
            vulDetection.vul_detection_id = vul_detection.get('vul_detection_id')
            vulDetection.script_name = vul_detection.get('script_name')
            vulDetection.user_id = vul_detection.get('user_id')
            vulDetection.serial_num = vul_detection.get('serial_num')
            vulDetection.is_alive = vul_detection.get('is_alive')
            vulDetection.is_index_404 = vul_detection.get('is_index_404')
            vulDetection.is_vuln = vul_detection.get('is_vuln')
            vulDetection.is_vuln_404 = vul_detection.get('is_vuln_404')
            vulDetection.ip = vul_detection.get('ip')
            vulDetection.port = vul_detection.get('port')
            vulDetection.description = vul_detection.get('description')
            db.session.add(vulDetection)

    @staticmethod
    def add_(vul_detection_list: list):
        with db.auto_commit():
            for vul_detection in vul_detection_list:
                vulDetection = VulDetection()
                vulDetection.vul_detection_id = vul_detection.get('vul_detection_id')
                vulDetection.script_name = vul_detection.get('script_name')
                vulDetection.user_id = vul_detection.get('user_id')
                vulDetection.serial_num = vul_detection.get('serial_num')
                vulDetection.is_alive = vul_detection.get('is_alive')
                vulDetection.is_index_404 = vul_detection.get('is_index_404')
                vulDetection.is_vuln = vul_detection.get('is_vuln')
                vulDetection.is_vuln_404 = vul_detection.get('is_vuln_404')
                vulDetection.ip = vul_detection.get('ip')
                vulDetection.port = vul_detection.get('port')
                vulDetection.description = vul_detection.get('description')
                db.session.add(vulDetection)
            else:
                data = {
                    'vul_detection_id':vul_detection_list[0].get('vul_detection_id'),
                    'script_name':vul_detection_list[0].get('script_name'),
                    'user_id':vul_detection_list[0].get('user_id')
                }
                VulSingleTest.add(data)

class VulIP(Base):
    __tablename__ = 'vul_ip'
    id = Column(Integer, primary_key=True)
    team_name = Column(String)
    script_name = Column(String)
    serial_num = Column(Integer)
    ip = Column(String)
    port = Column(Integer)
    user_id = Column(String)
    match_id = Column(String)
    match_name = Column(String)

    @staticmethod
    def add(vul_ip:dict):
        with db.auto_commit():
            vulIp = VulIP()
            vulIp.team_name = vul_ip.get('team_name')
            vulIp.script_name = vul_ip.get('script_name')
            vulIp.serial_num = vul_ip.get('serial_num')
            vulIp.ip = vul_ip.get('ip')
            vulIp.port = vul_ip.get('port')
            vulIp.match_name = vul_ip.get('match_name')
            vulIp.match_id = vul_ip.get('match_id')
            vulIp.user_id = vul_ip.get('user_id')
            db.session.add(vulIp)
            return vulIp

class VulDetectionAll(Base):
    __tablename__ = 'vul_detection_all'
    id = Column(Integer, primary_key=True)
    team_name = Column(String)
    match_name = Column(String)
    match_id = Column(String)
    script_name = Column(String)
    serial_num = Column(Integer)
    ip = Column(String)
    port = Column(Integer)
    description =Column(String)
    user_id = Column(String)
    is_alive = Column(SmallInteger)
    is_index_404 = Column(SmallInteger)
    is_vuln = Column(SmallInteger)
    is_vuln_404 = Column(SmallInteger)
    test_id = Column(String)

    def to_dict(self):
        return {
            'team_name':self.team_name,
            'match_name':self.match_name,
            'match_id':self.match_id,
            'script_name':self.script_name,
            'ip':self.ip,
            'port':self.port,
            'description':self.description,
            'is_alive':self.is_alive,
            'is_index_404':self.is_index_404,
            'is_vuln':self.is_vuln,
            'is_vuln_404':self.is_vuln_404,
            'test_id':self.test_id,
        }

    @staticmethod
    def add(vul_detect_all:dict):
        with db.auto_commit():
            vulDetectionAll = VulDetectionAll()
            vulDetectionAll.team_name = vul_detect_all.get('team_name')
            vulDetectionAll.match_name = vul_detect_all.get('match_name')
            vulDetectionAll.match_id = vul_detect_all.get('match_id')
            vulDetectionAll.script_name = vul_detect_all.get('script_name')
            vulDetectionAll.serial_num = vul_detect_all.get('serial_num')
            vulDetectionAll.ip = vul_detect_all.get('ip')
            vulDetectionAll.port = vul_detect_all.get('port')
            vulDetectionAll.description = vul_detect_all.get('description')
            vulDetectionAll.is_alive = vul_detect_all.get('is_alive')
            vulDetectionAll.is_index_404 = vul_detect_all.get('is_index_404')
            vulDetectionAll.is_vuln = vul_detect_all.get('is_vuln')
            vulDetectionAll.is_vuln_404 = vul_detect_all.get('is_vuln_404')
            vulDetectionAll.test_id = vul_detect_all.get('test_id')
            vulDetectionAll.user_id = vul_detect_all.get('user_id')
            db.session.add(vulDetectionAll)



class VulTest(Base):
    __tablename__ = 'vul_test'
    id = Column(Integer, primary_key=True)
    test_id = Column(String)
    match_name = Column(String)
    user_id = Column(String)

    def to_dict(self):
        return {
            'test_id':self.test_id,
            'match_name':self.match_name,
            'create_datetime':self.create_datetime
        }


    @staticmethod
    def add(vul_test:dict):
        with db.auto_commit():
            vulTest = VulTest()
            vulTest.test_id = vul_test.get('test_id')
            vulTest.match_name = vul_test.get('match_name')
            vulTest.user_id = vul_test.get('user_id')
            db.session.add(vulTest)


class VulUser(Base):
    __tablename__ = 'vul_users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    auth = Column(SmallInteger)
    user_id = Column(String)


    def insert_user(self):
        self.username = 'admin_004'
        self.password = generate_password_hash('admin_004')
        self.auth = 2
        self.user_id = uuid.uuid4()
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def verify(username, password):
        user = VulUser.query.filter_by(username=username).first()
        if not user:
            return False
        password_hash = user.password
        if not check_password_hash(password_hash, password):
            return False

        if user.auth == 1:
            scope = 'UserScope'
        elif user.auth == 2:
            scope = 'AdminScope'

        return {'uid':user.user_id, 'scope':scope}
















