# -*- coding: utf-8 -*-

# File: transaction.py	
# Created at 16/11/2021

"""
   Description: 
        -
        -
"""


class TransactionStatusEnum(object):
    SUCCESS = 'success'
    ERROR = 'error'
    PENDING = 'pending'


class TransactionTopicKeyEnum(object):
    SETTLEMENT = 'settlement_batch'
    ERROR_TRANSACTION = 'error_transaction'
    VOID_TRANSACTION = 'void_transaction'
    PRE_AUTH = 'pre_auth'


class SettlementStatusEnum(object):
    SUCCESS = 'success'
    ERROR = 'error'
    PENDING = 'pending'