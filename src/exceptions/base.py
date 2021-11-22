# -*- coding: utf-8 -*-



# File: base.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""


class BadRequestException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.response = {}

    pass
