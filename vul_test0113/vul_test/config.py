import os

class BaseConfig:
    SECRET_KEY = os.getenv('app_secret') or 'blg project'
    WTF_CSRF_ENABLED = False
    SCRIPTS_ABS_PATH = os.path.abspath('.') + '/scripts'
    SCRIPTS_PATH = 'scripts.'
    FUNCTION_NAME = 'check'
    EXTS = ['xlsx']

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://vulver:vulver@localhost/vulver'

class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database

class ProductionConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    ENCRYPTION_V1 = os.getenv('ENCRYPTION_V1')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}