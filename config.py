import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev'
    MAX_WORKERS = 5
    DEFAULT_MAX_RESULTS = 10
    HOST = '0.0.0.0'
    PORT = 8000

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 