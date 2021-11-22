# -*- coding: utf-8 -*-



# File: auth.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExceptionRequiredAuth(BadRequestException):
    def __init__(self, response=make_response(
        error_code='E_USER_AUTH',
        status=Constants.STATUS_NOT_OK,
        msg='Auth is required'
    ), *args: object) -> None:
        super().__init__(*args)
        self.response = response

    pass
