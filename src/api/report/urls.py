# -*- coding: utf-8 -*-



# File: urls.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""

from flask import Blueprint

from src.api.report.controller import *

rest_report_service = Blueprint('rest_report_service', __name__, url_prefix='/report')

rest_report_service.add_url_rule('init', methods=['POST'], view_func=create_report)