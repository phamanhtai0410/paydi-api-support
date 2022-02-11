# -*- coding: utf-8 -*-


# File: urls.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""

from flask import Blueprint

from src.api.report.controller import create_report, get_list_reports_for_admin

rest_report_service = Blueprint('rest_report_service', __name__, url_prefix='report')

rest_report_service.add_url_rule('init', methods=['POST'], view_func=create_report)

rest_report_service.add_url_rule('get_list_for_admin', methods=['GET'], view_func=get_list_reports_for_admin)
