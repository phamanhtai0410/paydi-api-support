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
from src.utils.format import is_oid, id_response, is_report_type, is_report_type


########################################################################
# Schema Request Data
########################################################################

class CreateReport(Schema):
    class Meta:
        unknown = INCLUDE

    type = fields.String(required=True, validate=is_report_type, error_messages={
        'validator_failed': 'input "type" is not valid !'
    })
    oid = fields.String(default='app_oid')
    message = fields.String()
    images = fields.List(fields.String())

########################################################################################
# Schema Response Data
########################################################################################

