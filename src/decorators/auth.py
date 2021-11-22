# -*- coding: utf-8 -*-


# File: auth.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""
import hashlib
import hmac
import json
from functools import wraps

from src.exceptions.auth import ExceptionRequiredAuth
from src.extensions import redis_global
from flask import request
from sentry_sdk import capture_exception
import jwt
import traceback
from src.utils.logger import Logger


def sha512(data, secret_key):
    _key = str(secret_key).encode('utf-8')
    byte_input = data.encode('utf-8')
    return hmac.new(_key, byte_input, hashlib.sha512).hexdigest()


def get_token_info(token):
    try:
        return jwt.decode(token, algorithm="RS256", options={"verify_signature": False})
    except:
        traceback.print_exc()
        capture_exception()
        return False


def verify_token():
    """
        - The function that verifies token
    """

    _rq_user_token = request.headers.get('Authorization')

    if not _rq_user_token or 'Bearer ' not in _rq_user_token:
        return None

    _rq_user_token = _rq_user_token.split(' ')[1]

    # Get user token on Redis user info
    _user = get_token_info(_rq_user_token)

    _user_info = _user.get('payload') if isinstance(_user, dict) else {}

    if not _user_info:
        return False

    _token_existed = redis_global.get(f"tokens:users:{_user_info.get('_id')}")

    if _token_existed and _token_existed == _rq_user_token:
        return _user_info

    return False


def verify_pos_token():
    """
        - The function that verifies token
    """

    _rq_pos_token = request.headers.get('Authorization')

    if not _rq_pos_token or 'Bearer ' not in _rq_pos_token:
        return None

    _rq_pos_token = _rq_pos_token.split(' ')[1]

    # Get pos token on Redis pos info
    _pos = get_token_info(_rq_pos_token)

    _pos_info = _pos.get('payload') if isinstance(_pos, dict) else {}

    if not _pos_info:
        return False

    _token_existed = redis_global.get(f"tokens:pos_accounts:{_pos_info.get('serial_number')}")

    if _token_existed and _token_existed == _rq_pos_token:
        return _pos_info

    return False


def verify_service():
    """
        - The function that verifies token
    """
    _rq_api_key = request.args.get('api_key', type=str)
    if not _rq_api_key:
        return False

    _api_secret_key = redis_global.get(f"api_secret_keys:{_rq_api_key}")

    if not _api_secret_key:
        return False

    if request.method == 'GET':
        _body = request.args.to_dict()
        del _body['api_key']

    else:
        _body = request.get_json()

    _code = _body.get('code')
    del _body['code']

    check_data = sorted(_body.items())

    check_string = json.dumps(check_data)

    hash_value = sha512(check_string, _api_secret_key)
    return _code == hash_value


def auth_user():
    """
        - Decorator to check and get user info from user token. Return
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if not request:  # Outside flask app context

                decorated_kwargs = {**kwargs, 'user_info': {}}

                return f(*args, **decorated_kwargs)

            user_info = verify_token()

            if not user_info:
                raise ExceptionRequiredAuth

            decorated_kwargs = {**kwargs, 'user_info': user_info}

            return f(*args, **decorated_kwargs)

        return wrapper

    return decorator


def auth_pos():
    """
        - Decorator to check and get user info from user token. Return
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if not request:  # Outside flask app context

                decorated_kwargs = {**kwargs, 'pos': {}}

                return f(*args, **decorated_kwargs)

            pos_info = verify_pos_token()

            if not pos_info:
                raise ExceptionRequiredAuth
            decorated_kwargs = {**kwargs, 'pos': pos_info}

            return f(*args, **decorated_kwargs)

        return wrapper

    return decorator

def get_pos():
    """
        - Decorator to check and get user info from user token. Return {} if no authen
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):

            if not request:  # Outside flask app context

                decorated_kwargs = {**kwargs, 'pos': {}}

                return f(*args, **decorated_kwargs)

            pos_info = verify_pos_token() 
            # if pos_info == None:
            #     Logger.debug('Authen check: ', pos_info)
            if not pos_info:
                pos_info = {}
                # raise ExceptionRequiredAuth
            decorated_kwargs = {**kwargs, 'pos': pos_info}

            return f(*args, **decorated_kwargs)

        return wrapper

    return decorator


def get_user():
    """
        - Decorator to check and get user info from user token. Return
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request:  # Outside flask app context
                decorated_kwargs = {**kwargs, 'user_info': {}}
                return f(*args, **decorated_kwargs)
            user_info = verify_token()
            if not user_info:
                user_info = {}
            decorated_kwargs = {**kwargs, 'user_info': user_info}
            return f(*args, **decorated_kwargs)

        return wrapper

    return decorator


def auth_service():
    """
        - Decorator to check other service
    """

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if not request:  # Outside flask app context
                return f(*args, **kwargs)

            service = verify_service()

            if not service:
                raise ExceptionRequiredAuth

            return f(*args, **kwargs)

        return wrapper

    return decorator
