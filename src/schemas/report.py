# -*- coding: utf-8 -*-


# File: report.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from os import terminal_size
from importlib_metadata import version
from marshmallow import Schema, fields, INCLUDE, EXCLUDE

from paydi_lib.schema import BaseResponse
from src.utils.format import is_report_type


########################################################################
# Schema Request Data
########################################################################
class GetListReport(Schema):
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
    message = fields.String(allow_none=True, missing='')
    images = fields.List(fields.String(), allow_none=True, missing=[])
    version = fields.String(allow_none=False)


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
    version = fields.String(allow_none=False)


class GetListReportsResponse(Schema, BaseResponse):
    class Meta:
        unknown: EXCLUDE

    reports = fields.List(fields.Nested(ReportResponse()))
    total = fields.Integer()
