# -*- coding: utf-8 -*-



# File: report.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from marshmallow import Schema, fields, ValidationError, INCLUDE, EXCLUDE, pre_load

from src.schemas.base import BaseResponse, BaseQuery
from src.utils.format import is_oid, id_response


########################################################################
# Schema Request Data
########################################################################

class CreateReport(Schema):
    class Meta:
        unknown = INCLUDE

    type = fields.String(required=True, default='app_error')
    oid = fields.String()
    message = fields.String()
    images = fields.List(fields.String())

########################################################################################
# Schema Response Data
########################################################################################

