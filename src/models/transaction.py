# -*- coding: utf-8 -*-

# File: transaction.py	
# Created at 13/11/2021

"""
   Description: 
        -
        -
"""
from pymodm import fields

from src.enums.transaction import TransactionStatusEnum
from paydi_lib.model import BaseMG


class TransactionModel(BaseMG):
    class Meta:
        collection_name = 'paydi_transactions'
        final = True
        ignore_unknown_fields = True

    """
        - Auto fill
    """

    _id = fields.ObjectIdField(primary_key=True)

    odoo_contact_id = fields.CharField(blank=True, default='')
    account_id = fields.CharField(blank=True, default='')
    pos_id = fields.CharField(blank=True, default='')

    obj_type = fields.CharField(blank=True, default='')  # pax, cash, qr code

    total_amount = fields.FloatField(blank=True, default='')
    error_msg = fields.CharField(blank=True, default='')
    status = fields.CharField(blank=True, default=TransactionStatusEnum.PENDING)
    extract = fields.DictField(blank=True, default={})
    has_voided = fields.BooleanField(default=False, blank=True)


class ErrorTransactionModel(BaseMG):
    class Meta:
        collection_name = 'paydi_error_transactions'
        final = True
        ignore_unknown_fields = True

    """
        - Auto fill
    """

    _id = fields.ObjectIdField(primary_key=True)

    odoo_contact_id = fields.CharField(blank=True, default='')
    account_id = fields.CharField(blank=True, default='')
    pos_id = fields.CharField(blank=True, default='')

    """
        - Request data app
    """
    # yyyymmddhhmmss

    req_merchant_trans_id = fields.CharField(blank=True, default='')
    req_tranx_type = fields.CharField(blank=True, default='')

    req_acqr_id = fields.CharField(blank=True, default='')
    req_transaction_amount = fields.FloatField(blank=True, default='')
    req_tip_amount = fields.FloatField(blank=True, default='')
    req_currency_name = fields.CharField(blank=True, default='')
    req_card_type = fields.IntegerField(blank=True, default='')
    # More
    card_holder = fields.CharField(blank=True, default='')
    card_number = fields.CharField(blank=True, default='')
    swipe_type = fields.CharField(blank=True, default='')
    exp_date = fields.CharField(blank=True, default='')
    # Error info
    code = fields.CharField(blank=True, default='')
    desc = fields.CharField(blank=True, default='')
    # ddmmyyN5Bank
    app_ver = fields.CharField(blank=True, default='')
    # SALE | REVERSAL
    tranx_type = fields.CharField(blank=True, default='')
    trans_date_time = fields.CharField(blank=True, default='')


class CardTransactionModel(BaseMG):
    class Meta:
        collection_name = 'paydi_card_transactions'
        final = True
        ignore_unknown_fields = True

    """
        - Auto fill
    """

    _id = fields.ObjectIdField(primary_key=True)

    odoo_contact_id = fields.CharField(blank=True, default='')
    account_id = fields.CharField(blank=True, default='')
    pos_id = fields.CharField(blank=True, default='')

    """
        - Request data app
    """
    # yyyymmddhhmmss

    req_merchant_trans_id = fields.CharField(blank=True, default='')
    req_tranx_type = fields.CharField(blank=True, default='')
    req_acqr_id = fields.CharField(blank=True, default='')
    req_transaction_amount = fields.FloatField(blank=True, default='')
    req_tip_amount = fields.FloatField(blank=True, default='')
    req_currency_name = fields.CharField(blank=True, default='')
    req_card_type = fields.IntegerField(blank=True, default='')

    """
        - Response from PAX
    """
    # response code
    code = fields.CharField(blank=True, default='')
    # Successfully
    desc = fields.CharField(blank=True, default='')
    # ddmmyyN5Bank
    app_ver = fields.CharField(blank=True, default='')
    # SALE | REVERSAL
    tranx_type = fields.CharField(blank=True, default='')

    approve_code = fields.CharField(blank=True, default='')
    batch_no = fields.CharField(blank=True, default='')
    """
        - Owner and card info
    """
    card_holder = fields.CharField(default='', blank=True)
    card_number = fields.CharField(blank=True, default='')
    """
        1: Thẻ quốc tế (không phải MasterCard)
        2: Thẻ nội địa
        3: Thẻ MasterCard
    """
    card_type = fields.CharField(blank=True, default='')
    currency = fields.CharField(blank=True, default='')

    exp_date = fields.CharField(blank=True, default='')
    ref_no = fields.CharField(blank=True, default='')
    invoice_no = fields.CharField(blank=True, default='')
    swipe_type = fields.CharField(blank=True, default='')
    total_amount = fields.FloatField(blank=True, default='')

    trans_date_time = fields.DateTimeField(blank=True, default='')

    trace_no = fields.CharField(blank=True, default='')

    terminal_id = fields.CharField(blank=True, default='')
    bank_merchant_id = fields.CharField(blank=True, default='')

    merchant_trans_id = fields.CharField(blank=True, default='')
    iso_response_code = fields.CharField(blank=True, default='')

    has_voided = fields.BooleanField(default=False, blank=True)
    void_data = fields.DictField(blank=True, default={})

    section_no = fields.CharField(default='', blank=True)
    metadata = fields.DictField(blank=True, default={})


class PreAuthTransactionModel(BaseMG):
    class Meta:
        collection_name = 'paydi_pre_auth_transactions'
        final = True
        ignore_unknown_fields = True

    """
        - Auto fill
    """

    _id = fields.ObjectIdField(primary_key=True)

    odoo_contact_id = fields.CharField(blank=True, default='')
    account_id = fields.CharField(blank=True, default='')
    pos_id = fields.CharField(blank=True, default='')

    """
        - Request data app
    """
    # yyyymmddhhmmss

    req_merchant_trans_id = fields.CharField(blank=True, default='')
    req_tranx_type = fields.CharField(blank=True, default='')
    req_acqr_id = fields.CharField(blank=True, default='')
    req_transaction_amount = fields.FloatField(blank=True, default='')
    req_tip_amount = fields.FloatField(blank=True, default='')
    req_currency_name = fields.CharField(blank=True, default='')
    req_card_type = fields.IntegerField(blank=True, default='')

    """
        - Response from PAX
    """
    # response code
    code = fields.CharField(blank=True, default='')
    # Successfully
    desc = fields.CharField(blank=True, default='')
    # ddmmyyN5Bank
    app_ver = fields.CharField(blank=True, default='')
    # SALE | REVERSAL
    tranx_type = fields.CharField(blank=True, default='')

    approve_code = fields.CharField(blank=True, default='')
    batch_no = fields.CharField(blank=True, default='')
    """
        - Owner and card info
    """
    card_holder = fields.CharField(default='', blank=True)
    card_number = fields.CharField(blank=True, default='')
    """
        1: Thẻ quốc tế (không phải MasterCard)
        2: Thẻ nội địa
        3: Thẻ MasterCard
    """
    card_type = fields.CharField(blank=True, default='')
    currency = fields.CharField(blank=True, default='')

    exp_date = fields.CharField(blank=True, default='')
    ref_no = fields.CharField(blank=True, default='')
    invoice_no = fields.CharField(blank=True, default='')
    swipe_type = fields.CharField(blank=True, default='')
    total_amount = fields.FloatField(blank=True, default='')

    trans_date_time = fields.DateTimeField(blank=True, default='')

    trace_no = fields.CharField(blank=True, default='')

    terminal_id = fields.CharField(blank=True, default='')
    bank_merchant_id = fields.CharField(blank=True, default='')

    merchant_trans_id = fields.CharField(blank=True, default='')
    iso_response_code = fields.CharField(blank=True, default='')
    has_voided = fields.BooleanField(default=False, blank=True)

    section_no = fields.CharField(default='', blank=True)
    void_data = fields.DictField(blank=True, default={})

    has_completed = fields.BooleanField(blank=True, default=False)
    complete_data = fields.DictField(blank=True, default={})
