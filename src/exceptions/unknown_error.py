# -*- coding: utf-8 -*-



# File: unknown_error.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExceptionUnknownError(BadRequestException):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            status=Constants.STATUS_NOT_OK,
            msg=Constants.MSG_UNKNOWN_ERROR,
            error_code='E_SERVER'
        )

    pass
