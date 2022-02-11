# -*- coding: utf-8 -*-


# File: report.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from marshmallow import Schema, fields, INCLUDE, EXCLUDE, pre_load

from paydi_lib.schema import BaseResponse, Convert


########################################################################
# Schema Request Data
########################################################################
class GetListTransactions(Schema):
    class Meta:
        unknown = INCLUDE

    limit = fields.Int(missing=0)
    offset = fields.Int(missing=0)


########################################################################################
# Schema Response Data
########################################################################################

class TransactionResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    _id = fields.String(required=True)
    created_time = fields.Float(required=True)

    odoo_contact_id = fields.String(allow_none=True)
    account_id = fields.String(required=True)
    pos_id = fields.String(required=True)

    obj_type = fields.String(required=True)

    total_amount = fields.Float(required=True)
    error_msg = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    extract = fields.Dict(allow_none=True)
    has_voided = fields.Boolean(allow_none=True, default=False)


class GetListTransactionsResponse(Schema, BaseResponse):
    class Meta:
        unknown: EXCLUDE

    transactions = fields.List(fields.Nested(TransactionResponse()))
    total = fields.Integer()


# --------------------------------------------------------------------------------------#

class ErrorTransactionResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE
    _id = fields.String(required=True)
    created_time = fields.Float(required=True)

    odoo_contact_id = fields.String(allow_none=True)
    account_id = fields.String(required=True)
    pos_id = fields.String(required=True)

    """
        - Request data app
    """
    # yyyymmddhhmmss

    req_merchant_trans_id = fields.String(allow_none=True, default='')
    req_tranx_type = fields.String(allow_none=True, default='')

    req_acqr_id = fields.String(allow_none=True, default='')
    req_transaction_amount = Convert(inner=fields.Float(), convert_to=float, missing=0, allow_none=True)
    req_tip_amount = Convert(inner=fields.Float(), convert_to=float, missing=0, allow_none=True)
    req_currency_name = fields.String(allow_none=True, default='')
    req_card_type = Convert(inner=fields.Float(), convert_to=float, missing=0, allow_none=True)
    # More
    card_holder = fields.String(allow_none=True, default='')
    card_number = fields.String(allow_none=True, default='')
    swipe_type = fields.String(allow_none=True, default='')
    exp_date = fields.String(allow_none=True, default='')
    # Error info
    code = fields.String(allow_none=True, default='')
    desc = fields.String(allow_none=True, default='')
    # ddmmyyN5Bank
    app_ver = fields.String(allow_none=True, default='')
    # SALE | REVERSAL
    tranx_type = fields.String(allow_none=True, default='')
    trans_date_time = fields.String(allow_none=True, default='')


class GetListErrorTransactionsResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    transactions = fields.List(fields.Nested(ErrorTransactionResponse()))
    total = fields.Integer()


# --------------------------------------------------------------------------------------#

class CardTransactionResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE
    _id = fields.String(required=True)
    created_time = fields.Float(required=True)

    odoo_contact_id = fields.String(allow_none=True)
    account_id = fields.String(required=True)
    pos_id = fields.String(required=True)

    """
        - Request data app
    """
    # yyyymmddhhmmss

    req_merchant_trans_id = fields.String(allow_none=True, default='')
    req_tranx_type = fields.String(allow_none=True, default='')
    req_acqr_id = fields.String(allow_none=True, default='')
    req_transaction_amount = fields.Float(allow_none=True, default='')
    req_tip_amount = fields.Float(allow_none=True, default='')
    req_currency_name = fields.String(allow_none=True, default='')
    req_card_type = fields.Integer(allow_none=True, default='')

    """
        - Response from PAX
    """
    # response code
    code = fields.String(allow_none=True, default='')
    # Successfully
    desc = fields.String(allow_none=True, default='')
    # ddmmyyN5Bank
    app_ver = fields.String(allow_none=True, default='')
    # SALE | REVERSAL
    tranx_type = fields.String(allow_none=True, default='')

    approve_code = fields.String(allow_none=True, default='')
    batch_no = fields.String(allow_none=True, default='')
    """
        - Owner and card info
    """
    card_holder = fields.String(default='', blank=True)
    card_number = fields.String(allow_none=True, default='')
    """
        1: Thẻ quốc tế (không phải MasterCard)
        2: Thẻ nội địa
        3: Thẻ MasterCard
    """
    card_type = fields.String(allow_none=True, default='')
    currency = fields.String(allow_none=True, default='')

    exp_date = fields.String(allow_none=True, default='')
    ref_no = fields.String(allow_none=True, default='')
    invoice_no = fields.String(allow_none=True, default='')
    swipe_type = fields.String(allow_none=True, default='')
    total_amount = fields.Float(allow_none=True, default='')

    trans_date_time = fields.Float(allow_none=True, default='')

    trace_no = fields.String(allow_none=True, default='')

    terminal_id = fields.String(allow_none=True, default='')
    bank_merchant_id = fields.String(allow_none=True, default='')

    merchant_trans_id = fields.String(allow_none=True, default='')
    iso_response_code = fields.String(allow_none=True, default='')

    has_voided = fields.Boolean(default=False, allow_none=True)
    void_data = fields.Dict(allow_none=True, default={})

    section_no = fields.String(default='', allow_none=True)
    metadata = fields.Dict(allow_none=True, default={})


class GetListCardTransactionsResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    transactions = fields.List(fields.Nested(CardTransactionResponse()))
    total = fields.Integer()


# --------------------------------------------------------------------------------------#

class PreAuthTransactionResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    _id = fields.String(required=True)
    created_time = fields.Float(allow_none=True)

    odoo_contact_id = fields.String(allow_none=True, missing='')
    account_id = fields.String(allow_none=True, missing='')
    pos_id = fields.String(allow_none=True, missing='')

    """
        - Request data app
    """
    # yyyymmddhhmmss

    req_merchant_trans_id = fields.String(allow_none=True, default='')
    req_tranx_type = fields.String(allow_none=True, default='')
    req_acqr_id = fields.String(allow_none=True, default='')
    req_transaction_amount = fields.Float(allow_none=True, default='')
    req_tip_amount = fields.Float(allow_none=True, default='')
    req_currency_name = fields.String(allow_none=True, default='')
    req_card_type = Convert(inner=fields.Integer(), convert_to=int, missing=0, allow_none=True)

    """
        - Response from PAX
    """
    # response code
    code = fields.String(allow_none=True, default='')
    # Successfully
    desc = fields.String(allow_none=True, default='')
    # ddmmyyN5Bank
    app_ver = fields.String(allow_none=True, default='')
    # SALE | REVERSAL
    tranx_type = fields.String(allow_none=True, default='')

    approve_code = fields.String(allow_none=True, default='')
    batch_no = fields.String(allow_none=True, default='')
    """
        - Owner and card info
    """
    card_holder = fields.String(default='', blank=True)
    card_number = fields.String(allow_none=True, default='')
    """
        1: Thẻ quốc tế (không phải MasterCard)
        2: Thẻ nội địa
        3: Thẻ MasterCard
    """
    card_type = fields.String(allow_none=True, default='')
    currency = fields.String(allow_none=True, default='')

    exp_date = fields.String(allow_none=True, default='')
    ref_no = fields.String(allow_none=True, default='')
    invoice_no = fields.String(allow_none=True, default='')
    swipe_type = fields.String(allow_none=True, default='')
    total_amount = fields.Float(allow_none=True, default='')

    trans_date_time = fields.Float(allow_none=True, default='')

    trace_no = fields.String(allow_none=True, default='')

    terminal_id = fields.String(allow_none=True, default='')
    bank_merchant_id = fields.String(allow_none=True, default='')

    merchant_trans_id = fields.String(allow_none=True, default='')
    iso_response_code = fields.String(allow_none=True, default='')
    has_voided = fields.Boolean(default=False, allow_none=True)

    section_no = fields.String(default='', allow_none=True)
    void_data = fields.Dict(allow_none=True, default={})

    has_completed = fields.Boolean(allow_none=True, default=False)
    complete_data = fields.Dict(allow_none=True, default={})


class GetListPreAuthTransactionsResponse(Schema, BaseResponse):
    class Meta:
        unknown = EXCLUDE

    transactions = fields.List(fields.Nested(PreAuthTransactionResponse()))
    total = fields.Integer()

# --------------------------------------------------------------------------------------#
