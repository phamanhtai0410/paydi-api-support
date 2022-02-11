# -*- coding: utf-8 -*-



# File: controller.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from datetime import datetime
from json import load
from src.decorators.response import handle_response
from src.exceptions import ExceptionNotFound

from bson import ObjectId
from flask import g, request

from src.decorators.request import load_data
from src.decorators.auth import get_pos
from src.schemas.transactions_statistic import GetListTransactions, GetListErrorTransactionsResponse, GetListCardTransactionsResponse, GetListPreAuthTransactionsResponse, GetListTransactionsResponse
from src.utils.logger import Logger, LoggerTask
from src.services.transaction import TransactionService
from src.exceptions.missing import ExceptionMissing


@handle_response()
def get_list_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    
    transactions, total = TransactionService.get_list_transactions(limit, offset)
    Logger.debug(f'List transactions <1> = {transactions}')
    if not isinstance(transactions, list):
        transactions = []


    return GetListTransactionsResponse.load_response({
        'transactions': transactions,
        'total': total
    })

@handle_response()
def get_list_error_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    transactions, total = TransactionService.get_list_error_transactions(limit, offset)
    Logger.debug(f'List transactions <2> = {transactions}')
    if not isinstance(transactions, list):
        transactions = []


    return GetListErrorTransactionsResponse.load_response({
        'transactions': transactions,
        'total': total
    })

@handle_response()
def get_list_card_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    transactions, total = TransactionService.get_list_card_transactions(limit, offset)

    if not isinstance(transactions, list):
        transactions = []


    return GetListCardTransactionsResponse.load_response({
        'transactions': transactions,
        'total': total
    })

@handle_response()
def get_list_pre_auth_transactions():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)

    transactions, total = TransactionService.get_list_pre_auth_transactions(limit, offset)

    if not isinstance(transactions, list):
        transactions = []


    return GetListPreAuthTransactionsResponse.load_response({
        'transactions': transactions,
        'total': total
    })