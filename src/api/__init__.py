# -*- coding: utf-8 -*-



# File: __init__.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from .common import rest_service
from .report import rest_report_service
from .transactions_statistic import rest_transactions_statistic_service
rest_app = (
    rest_service,
    rest_report_service,
    rest_transactions_statistic_service
)
