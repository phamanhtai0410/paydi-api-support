from bson.objectid import ObjectId
from src.enums import MethodEnum
from src.utils.datetime import get_current_time
from src.utils.logger import LoggerTask
from src.models.report import Report
from src.utils.send__telegram_mess import *
from src.config import DefaultConfig
from src.enums.report import ReportEnumKey
from src.constants import Constants

class ReportWorker(object):

    @staticmethod
    def create_report(data):
        Report.add(data)

    @staticmethod
    def send_report_mess(data):
        message = '<strong>{}: {} </strong> ' \
                  '<pre>' \
                  '<i>Merchant      : " {} "</i> \n' \
                  '<i>Account ID    : " {} "</i> \n' \
                  '<i>Pos ID        : " {} "</i> \n' \
                  '<i>Serial Number : " {} "</i> \n' \
                  '<i>Message       : " {} "</i> \n' \
                  '</pre> ' \
                  '<a href="#">👉👉👉 Chi tiết</a> \n' \
            .format("Report mới",  Constants.REPORT_TYPE_DICT.get(data.get('type')), data.get('merchant_id'), data.get('account_id'), data.get('serial_number'), data.get('pos_id'),
                    data.get('message'))

        result = send_telegram_message(token_id=DefaultConfig.TELE_SUPPORT_TOKEN_ID,
                                       chat_id=DefaultConfig.TELE_SUPPORT_CHAT_ID, message=message)
        LoggerTask.debug(f'send to Tele res = {result}')

    @classmethod
    def run_task(cls, message):
        """
            - The function handle
        """
        # if message.get('key') == ReportEnumKey.REPORT_CREATE:
        cls.create_report(message.get('value'))

        # if message.get('key') == ReportEnumKey.REPORT_SEND_MESS:
        cls.send_report_mess(message.get('value'))

        LoggerTask.debug(f'run_task {message}')
        pass
