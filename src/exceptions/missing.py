# -*- coding: utf-8 -*-



# File: missing.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from src.utils.response import make_response
from src.exceptions.base import BadRequestException
from src.constants import Constants


class ExceptionMissing(BadRequestException):
    def __init__(self, message='Missing data', errors={}, *args: object) -> None:
        super().__init__(*args)
        self.response = make_response(
            error_code='E_DATA_INVALID',
            status=Constants.STATUS_NOT_OK,
            msg=message,
            errors=errors
        )

    pass
