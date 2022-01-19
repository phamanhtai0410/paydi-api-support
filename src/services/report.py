# -*- coding: utf-8 -*-


# File: report.py	
# Created at 16/11/2021
"""
   Description: 
        -
        -
"""
from src.producers.report import send_create_report_task
from src.models.report import Report
from src.enums.report import ReportEnumKey
from paydi_lib.logger import LoggerTask

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
    def create_one(info: dict, pos: dict) -> dict:
        # send_push_telegram_report_mess_task('support_topic', info, ReportEnumKey.REPORT_SEND_MESS)
        _form_data = {
            key: value for (key, value) in info.items()
        }
        _form_data['serial_number'] = pos.get('serial_number', '')
        _form_data['account_id'] = pos.get('account_id', '')
        _form_data['terminal_id'] = pos.get('tid')
        _form_data['pos_id'] = pos.get('pos_id', '')
        _form_data['merchant_id'] = pos.get('merchant_id')
        _form_data['odoo_contact_id'] = pos.get('odoo_contact_id')
        send_create_report_task('support_topic', _form_data, ReportEnumKey.REPORT_CREATE)
        return {}
