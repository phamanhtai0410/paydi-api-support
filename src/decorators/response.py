# -*- coding: utf-8 -*-



# File: response.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from datetime import datetime
from functools import wraps
from src.utils.response import make_response

from marshmallow.fields import Constant
from src.constants import Constants
from src.exceptions.handler import request_exception
from flask import jsonify
from flask.globals import request
from src.decorators import cache_request


def handle_response(caching=False, timeout=604800, default=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            @request_exception(default=default)
            def run_controller():
                @cache_request(
                    keep_timeout=timeout,
                    key_prefix=request.path
                )
                def run_with_cache():
                    return f(*args, **kwargs)
                if caching:
                    data = run_with_cache()
                else:
                    data = f(*args, **kwargs)
                if isinstance(data, tuple):
                    # data, msg
                    return make_response(data=data[0], msg=data[1])
                # data: dict
                return make_response(data)

            return jsonify(run_controller()), 200
        return wrapper

    return decorator
