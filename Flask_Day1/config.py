import os
from utils import crypt


def verify(cofig):
    aes_crypt = crypt.AES_MODE_EAS()
    if aes_crypt.verify_integrity(cofig.SQLALCHEMY_DATABASE_URI):
        SQLALCHEMY_DATABASE_URI = aes_crypt.process_config(cofig.SQLALCHEMY_DATABASE_URI)
        cofig.SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI


class Baseconfig:
    # SECRET_KEY = os.getenv(
    #     'app secret') or b"\xc7i9\x8f7\xfe!\xa0\x96F\x1e\xcc\xdf\xd1o\r'\xaf\xfe5\xbf`\x0b\xad\x10\x83\xd2\x7f\xe0\xcc\r\xf8"
    SECRET_KEY = b"\xc7i9\x8f7\xfe!\xa0\x96F\x1e\xcc\xdf\xd1o\r'\xaf\xfe5\xbf`\x0b\xad\x10\x83\xd2\x7f\xe0\xcc\r\xf8"
    WTF_CSRF_ENABLED = False
    SCRIPTS_ABS_PATH = os.path.join(os.path.abspath('.') , 'scripts')
    SCRIPTS_PATH = 'scripts.'
    FUNCTION_NAME = 'check'
    EXTS = ['xlsx']


class Developmentconfig(Baseconfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XcjqfvecveJ9VTUU8tDYC6:0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XppfijRP/jG+BYWkQmBoux@0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XCjqv6Ga+9WK1lbnARN460/0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37Xbkq3EAaKhX9FXVUspCYS+'
    # dialect+driver://username:password@host:port/database
    # SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XahLvvecveJ9VTUU8tDYC6:0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XppfijRP/jG+BYWkQmBoux@0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37XCjqv6Ga+9WK1lbnARN460/0yHHdeaqv6PdXELCbo/GOBx+0sLCMzvsBzg2bC+f37Xbkq3EAaKhX9FXVUspCYS+'


class TestingConfig(Baseconfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class Productionconfig(Baseconfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE URL')
    ENCRYPTION_V1 = os.getenv('ENCRYPTION V1')


db_config = {'development': Developmentconfig,
             'testing': TestingConfig,
             'production': Productionconfig
             }
