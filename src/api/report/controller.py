# -*- coding: utf-8 -*-



# File: controller.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
from datetime import datetime
from src.decorators.response import handle_response
from src.exceptions import ExceptionNotFound

from bson import ObjectId
from flask import g

from src.decorators.request import load_data
from src.decorators.auth import get_pos
from src.schemas.report import *
from src.utils.logger import Logger, LoggerTask
from src.services.report import ReportService
from src.exceptions.missing import ExceptionMissing

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
        raise ExceptionMissing

    ReportService.create_one(data, pos)
    return data

