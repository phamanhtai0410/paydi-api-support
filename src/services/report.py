# -*- coding: utf-8 -*-


# File: report.py	
# Created at 16/11/2021
"""
   Description: 
        -
        -
"""
from logging import Logger
from src.models.report import Report
from src.producers.report import send_create_report_task
from src.models.report import Report
from src.enums.report import ReportEnumKey
from src.utils.logger import LoggerTask

class ReportService(object):
    @staticmethod
    def get_list_report_for_admin(limit: int, offset: int) -> list:
        reports = Report.get_by_filter(
            filter={},
            options={
                'limit': limit,
                'offset': offset
            }
        )
        total = Report.current().count()
        LoggerTask.debug(f'Report Service get list for admin {reports}')
        return reports, total

    @staticmethod
    def create_one(data: dict) -> dict:
        send_create_report_task('support_topic', data, ReportEnumKey.REPORT_CREATE)
        return {}
