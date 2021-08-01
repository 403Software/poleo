"""
It is responsible for the configuration

...

Methods
-------
get_current_config()
    Gets current config
"""

import load_envs
from os import getenv, path
from utils.boolean_util import str_to_bool

load_envs.load()


class Config:
    """
    It provides base config
    """

    API = 'oner-flask-rest-api'
    VERSION = getenv('MVP.SPRINT.FEATURES', '1.42.1')


    HOST = getenv('HOST')
    APP_PORT = int(getenv('APP_PORT')) if getenv('APP_PORT') else ""
    DEBUG = eval(getenv('DEBUG').title()) if getenv('DEBUG') else ""
    LOGS_PATH = path.abspath(getenv('LOGS_PATH', ''))
    STAGE = getenv('STAGE', 'dev')

    # DATABASE
    DATABASE_CONNECTION_STRING = getenv('DATABASE_CONNECTION_STRING')
    DATABASE_USERNAME = getenv('DATABASE_USERNAME')
    DB_PASSWORD = getenv('DB_PASSWORD')
    LOG_LEVEL = getenv('LOG_LEVEL')

class DevelopmentConfig(Config):
    """
    Development mode config
    """

    FLASK_ENV = 'development'
    DEBUG = True


class TestingConfig(Config):
    """
    Testing mode config
    """

    FLASK_ENV = 'testing'
    DEBUG = False
    CA_MOCK_SERVICES = False


class HomologationConfig(Config):
    """
    Homologation mode config
    """

    FLASK_ENV = 'homologation'
    DEBUG = False


class ProductionConfig(Config):
    """
    Production mode config
    """

    FLASK_ENV = 'production'
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'dev': DevelopmentConfig,
    'testing': TestingConfig,
    'homologation': HomologationConfig,
    'hml': HomologationConfig,
    'production': ProductionConfig,
    'prd': ProductionConfig,
    'default': DevelopmentConfig
}


def get_current_config():
    """
    Gets current config

    Returns
    -------
    Config
        current config
    """

    return config[getenv('FLASK_ENV', 'default').lower()]
