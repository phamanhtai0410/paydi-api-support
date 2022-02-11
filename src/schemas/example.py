# -*- coding: utf-8 -*-


# File: example.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""
from marshmallow import Schema, fields, INCLUDE, EXCLUDE

from paydi_lib.schema import BaseResponse
from paydi_lib.util import is_oid


class Example(Schema):
    class Meta:
        unknown = INCLUDE

    limit = fields.Int()
    offset = fields.Int(missing=0)
    type = fields.String()
    _id = fields.String(validate=is_oid, error_messages={
        'validator_failed': '_id must be a objectId as string'
    })


class ExampleResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    _id = fields.String()
    created_time = fields.Float()
