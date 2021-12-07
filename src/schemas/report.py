# -*- coding: utf-8 -*-



# File: report.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from os import terminal_size
from marshmallow import Schema, fields, ValidationError, INCLUDE, EXCLUDE, pre_load

from src.schemas.base import BaseResponse, BaseQuery
from src.utils.format import is_oid, id_response, is_report_type, is_report_type


########################################################################
# Schema Request Data
########################################################################
class GetListReport(Schema, BaseQuery):
    class Meta:
        unknown = INCLUDE

    limit = fields.Int(missing=0)
    offset = fields.Int(missing=0)

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

class ReportResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    _id = fields.String()
    created_time = fields.Float()
    type = fields.String(required=True)
    oid = fields.String()
    terminal_id = fields.String(allow_none=True)
    merchant_id = fields.String(allow_none=True)
    serial_number = fields.String()
    account_id = fields.String()
    pos_id = fields.String()
    message = fields.String()
    images = fields.List(fields.String())


class GetListReportsResponse(Schema, BaseResponse):
    class Meta:
        unknown: EXCLUDE

    reports = fields.List(fields.Nested(ReportResponse()))
    total = fields.Integer()