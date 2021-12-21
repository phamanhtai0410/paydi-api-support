# -*- coding: utf-8 -*-



# File: urls.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""

from flask import Blueprint

from src.api.transactions_statistic.controller import get_list_transactions, get_list_error_transactions, get_list_card_transactions, get_list_pre_auth_transactions

rest_transactions_statistic_service = Blueprint('rest_transactions_statistic_service', __name__, url_prefix='transactions_statistic')

rest_transactions_statistic_service.add_url_rule('transactions', methods=['GET'], view_func=get_list_transactions)

rest_transactions_statistic_service.add_url_rule('error_transactions', methods=['GET'], view_func=get_list_error_transactions)

rest_transactions_statistic_service.add_url_rule('card_transactions', methods=['GET'], view_func=get_list_card_transactions)

rest_transactions_statistic_service.add_url_rule('pre_auth_transactions', methods=['GET'], view_func=get_list_pre_auth_transactions)