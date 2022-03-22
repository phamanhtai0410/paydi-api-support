from paydi_lib.logger import LoggerTask
from src.models.report import Report
from src.models.crm import CRM
from paydi_lib.logger import Logger
from src.utils.send__telegram_mess import *
from src.config import DefaultConfig
from src.constants import Constants
import xmlrpc.client
from src.utils.request import make_request

class ReportWorker(object):

    @staticmethod
    def create_report(data):
        Report.add(data)

    @staticmethod
    def send_report_mess(data):
        if (data.get('type') == 'transaction'):
            message = '<strong>{}: {} #{} </strong> \n' \
                      '<pre>' \
                      '<i>Odoo Contact ID      : " {} "</i> \n' \
                      '<i>Account ID           : " {} "</i> \n' \
                      '<i>Serial Number        : " {} "</i> \n' \
                      '<i>Device ID            : " {} "</i> \n' \
                      '<i>Pos ID               : " {} "</i> \n' \
                      '<i>App Version          : " {} "</i> \n' \
                      '<i>Message              : " {} "</i> \n' \
                      '</pre> ' \
                      '<a href="#">👉👉👉 Chi tiết</a> \n' \
                .format("Report mới",
                        Constants.REPORT_TYPE_DICT.get(data.get('type')),
                        data.get('oid'),
                        data.get('odoo_contact_id'),
                        data.get('account_id'),
                        data.get('serial_number'),
                        data.get('device_id'),
                        data.get('pos_id'),
                        data.get('version'),
                        data.get('message'))
        else:
            message = '<strong>{}: {} </strong> \n' \
                      '<pre>' \
                      '<i>Odoo Contact ID      : " {} "</i> \n' \
                      '<i>Account ID           : " {} "</i> \n' \
                      '<i>Serial Number        : " {} "</i> \n' \
                      '<i>Device ID            : " {} "</i> \n' \
                      '<i>Pos ID               : " {} "</i> \n' \
                      '<i>App Version          : " {} "</i> \n' \
                      '<i>Message              : " {} "</i> \n' \
                      '</pre> ' \
                      '<a href="#">👉👉👉 Chi tiết</a> \n' \
                .format("Report mới",
                        Constants.REPORT_TYPE_DICT.get(data.get('type')),
                        data.get('odoo_contact_id'),
                        data.get('account_id'),
                        data.get('serial_number'),
                        data.get('device_id'),
                        data.get('pos_id'),
                        data.get('version'),
                        data.get('message'))

        result = send_telegram_message(token_id=DefaultConfig.TELE_SUPPORT_TOKEN_ID,
                                       chat_id=DefaultConfig.TELE_SUPPORT_CHAT_ID, message=message)
        LoggerTask.debug(f'send to Tele res = {result}')

    @staticmethod
    def create_report_in_odoo(data):
        LoggerTask.debug(f'Create new ticket in Odoo{data}')
        
        # Get connection to Odoo CRM from db
        crm_url = CRM.get_one(filter={
            'company_code': data.get('company_code')
        }).get('crm_url')
        if not crm_url:
            return None
        
        def get_html_images(images: list) -> str:
            list_images_link = []
            for i in images:
                list_images_link.append(f'<div><a href="{i}">{i}</a></div>')
            return ''.join(list_images_link)
        
        images = get_html_images(data.get('images'))
        
        
        
        description = f"<div><strong>1. </strong>Type : {Constants.REPORT_TYPE_DICT.get(data.get('type'))}</div> \
                            <div><strong>2. </strong>OID : {data.get('oid') if data.get('oid') != 'app_oid' else 'None'}</div> \
                            <div><strong>3. </strong>Terminal ID : {data.get('terminal_id')}</div> \
                            <div><strong>4. </strong>Serial Number : {data.get('serial_number')}</div> \
                            <div><strong>5. </strong>Account ID : {data.get('account_id')}</div> \
                            <div><strong>6. </strong>POS ID : {data.get('pos_id')}</div> \
                            <div><strong>7. </strong>App Version : {data.get('version')}</div> \
                            <div><strong>8. </strong>Message : {data.get('message')}</div> \
                            <div><strong>9. </strong>Images : {images}</div>"
                            
        resp = make_request(
            url=crm_url + '/iapi/v1/helpdesk/tickets/create',
            method='POST',
            body={
                "subject": "# Customer Report",
                "description": description
            },
            params={},    
        )
        
        LoggerTask.debug(f'Create new ticket resp in Odoo {resp}')
        
        pass

    @classmethod
    def run_task(cls, message):
        """
            - The function handle
        """
        cls.create_report(message.get('value'))

        cls.send_report_mess(message.get('value'))

        cls.create_report_in_odoo(message.get('value'))

        LoggerTask.debug(f'run_task {message}')
        pass
