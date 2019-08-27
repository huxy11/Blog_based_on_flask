import os

basedir =os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'and i am iron man!'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    ADMIN_NAME = 'huxy'
    ADMIN_PASSWORD = os.environ.get('FLASKY_ADMIN_PASSWORD') or 'huxy'
    #FLASKY_ADMIN = os.environ.get('FLASKY_ADMIN')

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    #SQLALCHEMY_DATABASE_URI =os.environ.get('DEV_DATABASE_URL')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir, 'data-dev.sqlite')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir, 'data-test.sqlite')

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+ os.path.join(basedir, 'data.sqlite')

config = {
        'dev' : DevelopmentConfig,
        'tst' : TestingConfig,
        'prd' : ProductionConfig,

        'dft' : DevelopmentConfig
        }
