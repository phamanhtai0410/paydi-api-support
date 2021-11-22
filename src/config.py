# -*- coding: utf-8 -*-


# File: config.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()


class BaseConfig(object):
    PROJECT = "support"

    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = False
    TESTING = False

    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = '\xd2\x0c\xa9\xb7\xd9E\xda-\x1e\xdb;\xb8\x0c\xfc\xbf\xf3\x16[\xa2x\xd5s\x83\xe3'


class DefaultConfig(BaseConfig):
    """
        - Base config
    """
    DEBUG = True
    PREFIX = f'/v1/{BaseConfig.PROJECT}'
    # Flask-babel: http://pythonhosted.org/Flask-Babel/
    ACCEPT_LANGUAGES = ['vi']
    TELE_SUPPORT_TOKEN_ID = os.getenv('TELE_SUPPORT_TOKEN_ID')
    TELE_SUPPORT_CHAT_ID = os.getenv('TELE_SUPPORT_CHAT_ID')


    BABEL_DEFAULT_LOCALE = 'en'
    SENTRY_DSN = os.getenv('SENTRY_DSN')
    """
        - Redis config
    """
    CACHING = True
    CACHE_SUB = ''
    REDIS_URL = os.getenv('REDIS_URL')
    REDIS_GLOBAL = json.loads(os.getenv('REDIS_GLOBAL', default='[]'))
    REDIS_CLUSTER = json.loads(os.getenv('REDIS_CLUSTER', default='[]'))
    """
        - Database config
    """
    MONGODB_URI = os.getenv('MONGODB_URI')
    """
        - Inside config
    """
    INSIDE_APIKEY = os.getenv('INSIDE_APIKEY')
    """
        - Config kafka
    """
    KAFKA_SERVER = os.getenv('KAFKA_SERVER')
