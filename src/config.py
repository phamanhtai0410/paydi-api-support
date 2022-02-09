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
    # KAFKA_SERVER = os.getenv('KAFKA_SERVER')
    KAFKA_SERVER = json.loads(os.getenv('KAFKA_SERVER', default='[]'))

    """
        - Odoo calling config
    """
    ODOO_MMS_URL = os.getenv('ODOO_MMS_URL')
    ODOO_MMS_DB = os.getenv('ODOO_MMS_DB')
    ODOO_MMS_USERNAME = os.getenv('ODOO_MMS_USERNAME')
    ODOO_MMS_PASSWORD = os.getenv('ODOO_MMS_PASSWORD')
    
    ODOO_TICKET_TEAM_ID = os.getenv('ODOO_TICKET_TEAM_ID')
    ODOO_TICKET_PARTNER_NAME = os.getenv('ODOO_TICKET_PARTNER_NAME')
    ODDO_TICKET_PARTNER_ID = os.getenv('ODDO_TICKET_PARTNER_ID')
    ODDO_TICKET_PARTNER_EMAIL = os.getenv('ODDO_TICKET_PARTNER_EMAIL')


