# -*- coding: utf-8 -*-


# File: controller.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from paydi_lib.decorators import handle_response

from flask import g, request

from src.schemas.transactions_statistic import GetListErrorTransactionsResponse, \
    GetListCardTransactionsResponse, GetListPreAuthTransactionsResponse, GetListTransactionsResponse
from paydi_lib.logger import Logger
from src.services.transaction import TransactionService


@handle_response(schema=GetListTransactionsResponse)
def get_list_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    transactions, total = TransactionService.get_list_transactions(limit, offset)
    Logger.debug(f'List transactions <1> = {transactions}')
    if not isinstance(transactions, list):
        transactions = []

    return {
        'transactions': transactions,
        'total': total
    }


@handle_response(schema=GetListErrorTransactionsResponse)
def get_list_error_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    transactions, total = TransactionService.get_list_error_transactions(limit, offset)
    Logger.debug(f'List transactions <2> = {transactions}')
    if not isinstance(transactions, list):
        transactions = []

    return {
        'transactions': transactions,
        'total': total
    }


@handle_response(schema=GetListCardTransactionsResponse)
def get_list_card_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    transactions, total = TransactionService.get_list_card_transactions(limit, offset)

    if not isinstance(transactions, list):
        transactions = []

    return {
        'transactions': transactions,
        'total': total
    }


@handle_response(schema=GetListPreAuthTransactionsResponse)
def get_list_pre_auth_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    transactions, total = TransactionService.get_list_pre_auth_transactions(limit, offset)

    if not isinstance(transactions, list):
        transactions = []

    return {
        'transactions': transactions,
        'total': total
    }
