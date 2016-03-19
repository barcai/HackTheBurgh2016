import os


BASEDIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = '\x8a\x023\\\x83C\xd5\x16Fm\xc4\xeb\xeear\x13\x8a\x12\xe3d\xcd\xc9\x08b'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = False
    PROPAGATE_EXCEPTIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR,
                                                          'budgetbanger-dev.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASEDIR,
                                                          'budgetbanger.db')


config_dict = {
    'dev': DevelopmentConfig,
    'test': TestingConfig,
    'prod': ProductionConfig,
    'default': DevelopmentConfig
}