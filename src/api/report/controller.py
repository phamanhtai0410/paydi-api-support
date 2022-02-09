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
# ------------------------------
from paydi_lib.exceptions import MissingData


@handle_response()
@load_data(CreateReport)
@get_pos()
def create_report(pos):
    data = g.data
    Logger.debug('Create report - info ', data)
    Logger.debug('Create report - pos ', pos)
    
    create_data = {
        **data,
        **pos
    }
    Logger.debug('Create report - create_data ', create_data) 
    if not create_data.get('serial_number') or not create_data.get('company_code'):
        raise MissingData
        
    ReportService.create_one(create_data)    
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
