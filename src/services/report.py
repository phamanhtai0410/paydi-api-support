# -*- coding: utf-8 -*-


# File: report.py	
# Created at 16/11/2021
"""
   Description: 
        -
        -
"""
from src.models.report import Report
from src.producers.report import send_create_report_task, send_push_telegram_report_mess_task
from bson import ObjectId
from src.utils.logger import LoggerTask
from src.models.report import Report


class ReportService(object):

	@staticmethod
	def create_one(info: dict, pos: dict) -> dict:
		key = ObjectId()
		send_push_telegram_report_mess_task('support_topic', info, key)
		_form_data = { key:value for (key, value) in info.items() }
		_form_data['serial_number'] = pos.get('serial_number')
		_form_data['account_id'] = pos.get('account_id')
		_form_data['terminal_id'] = pos.get('tid')
		_form_data['pos_id'] = pos.get('pos_id')
		report = Report.add(_form_data)
		# send_create_report_task('support_topic', info, key)
		return report
