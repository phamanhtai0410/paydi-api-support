# -*- coding: utf-8 -*-



# File: bad_request.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExceptionBadRequest(BadRequestException):
    def __init__(self, message='Bad request', *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='E_REQUEST',
            status=Constants.STATUS_NOT_OK,
            msg=message
        )
    pass
