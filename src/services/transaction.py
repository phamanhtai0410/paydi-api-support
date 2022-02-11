# -*- coding: utf-8 -*-


# File: report.py	
# Created at 16/11/2021
"""
   Description: 
        -
        -
"""
from src.models.transaction import TransactionModel, ErrorTransactionModel, CardTransactionModel, \
    PreAuthTransactionModel


class TransactionService(object):
    @staticmethod
    def get_list_transactions(limit: int, offset: int) -> list:
        transactions = TransactionModel.get_by_filter(
            filter={},
            options={
                'limit': limit,
                'offset': offset
            }
        )
        total = TransactionModel.current().count()
        return transactions, total

    @staticmethod
    def get_list_error_transactions(limit: int, offset: int) -> list:
        transactions = ErrorTransactionModel.get_by_filter(
            filter={},
            options={
                'limit': limit,
                'offset': offset
            }
        )
        total = ErrorTransactionModel.current().count()
        return transactions, total

    @staticmethod
    def get_list_card_transactions(limit: int, offset: int) -> list:
        transactions = CardTransactionModel.get_by_filter(
            filter={},
            options={
                'limit': limit,
                'offset': offset
            }
        )
        total = CardTransactionModel.current().count()
        return transactions, total

    @staticmethod
    def get_list_pre_auth_transactions(limit: int, offset: int) -> list:
        transactions = PreAuthTransactionModel.get_by_filter(
            filter={},
            options={
                'limit': limit,
                'offset': offset
            }
        )
        total = PreAuthTransactionModel.current().count()
        return transactions, total
