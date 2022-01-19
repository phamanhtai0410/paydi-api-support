# -*- coding: utf-8 -*-


# File: controller.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from paydi_lib.decorators import handle_response, load_data, get_pos

from flask import g, request

from src.schemas.report import *
from paydi_lib.logger import Logger, LoggerTask
from src.services.report import ReportService
from paydi_lib.exceptions import MissingData


@handle_response()
@load_data(CreateReport)
@get_pos()
def create_report(pos):
    data = g.data
    Logger.debug('Create report - info ', data)
    Logger.debug('Create report - pos ', pos)
    if pos == {}:
        if data.get('merchant_id') and data.get('terminal_id'):
            pos_info = {
                'merchant_id': data.get('merchant_id'),
                'tid': data.get('terminal_id')
            }
            ReportService.create_one(data, pos_info)
            return data
        raise MissingData

    ReportService.create_one(data, pos)
    return data


@handle_response()
def get_list_reports_for_admin():
    limit = request.args.get('limit', 10, type=int)
    offset = request.args.get('offset', 0, type=int)
    reports, total = ReportService.get_list_report_for_admin(limit, offset)
    LoggerTask.debug(f'Reports list for admin ={reports}')
    if not isinstance(reports, list):
        reports = []
    LoggerTask.debug(f'Get list reports for admin {reports}')
    return GetListReportsResponse.load_response({
        'reports': reports,
        'total': total
    })
