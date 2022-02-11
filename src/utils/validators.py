# -*- coding: utf-8 -*-



# File: validators.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from bson import ObjectId

from src.exceptions.handler import handle_exception


@handle_exception(tracking=False, default=False)
def is_oid(oid):
    return ObjectId.is_valid(oid)
