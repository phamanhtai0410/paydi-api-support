from bson.objectid import ObjectId
from src.enums import MethodEnum
from src.utils.datetime import get_current_time
from src.utils.logger import LoggerTask
from src.models.report import Report
from src.utils.send__telegram_mess import *
from src.config import DefaultConfig
from src.enums.report import ReportEnumKey
from src.constants import Constants
import xmlrpc.client
import json
import time


def myprint(data_list, title=''):
    if title:
        print(title)
    for line in data_list:
        print('-', line)
    pass

class XMLRPC_API():
    def __init__(self, url, db, username='admin', password='admin'):
        self.url = url
        self.db = db
        self.username = username
        self.password = password
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(self.url))
        self.uid = common.authenticate(self.db, self.username, self.password, {})
        self.models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(self.url))
        pass

    # get fields names of the model
    def get_fields(self, model_name, required=False):
        data = self.models.execute_kw(self.db, 
            self.uid, 
            self.password, 
            model_name, 
            'fields_get',
            [], {'attributes': ['string', 'type', 'required', 'readonly']})
        
        if required:
            key_list = list(data.keys())
            for k in key_list:
                if not data[k].get('required', False):
                    data.pop(k)
                pass
        return data

    def search(self, model_name, conditions=[()]):
        return self.models.execute_kw(self.db, self.uid, self.password,
            model_name, 
            'search',
            [conditions])  

    # Create
    def create(self, model_name, data_dict):
        """
        Eg.
            model_name: 'res.users'
            data_dict: { 'name': "Minh", 'age': 27 }
        """
        id = self.models.execute_kw(self.db, self.uid, self.password, model_name, 'create', [data_dict])
        return id

    # Read
    def read(self, model_name, conditions=[()], params={}):
        """
        Eg.
            model_name: 'res.users'
            conditions: [('id', '>', 1)]
            params: {'fields': ['name', 'country_id', 'comment'], 'limit': 5}
        """
        return self.models.execute_kw(self.db, self.uid, self.password,
            model_name, 
            'search_read',
            [conditions],
            params)       
    
    # Update
    def update(self, model_name, id_list, new_data_dict):
        """
        Eg.
            model_name: 'res.users'
            id_list: [7]
            new_data_dict: { 'name': "Newer partner", 'age': 27 }
        """
        self.models.execute_kw(self.db, 
            self.uid, 
            self.password, 
            model_name, 
            'write', 
            [id_list, new_data_dict])

    # Delete
    def delete(self, model_name, id_list):
        self.models.execute_kw(self.db, self.uid, self.password, model_name, 'unlink', [id_list])
        pass

    # Soft delete
    def soft_delete(self, model_name, id_list):
        self.update(model_name, id_list, {
            'active': False,
        })

    # Aug 01, 2019
    def call(self, model_name, method, params=[]):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, method, params)

    def call2(self, model_name, method, param1, param2):
        return self.models.execute_kw(self.db, self.uid, self.password, model_name, method, param1, param2)



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

    @staticmethod
    def create_report_in_odoo(data):
        client = XMLRPC_API(url=DefaultConfig.ODOO_URL,
                            db=DefaultConfig.ODOO_DB,
                            username=DefaultConfig.ODOO_USERNAME,
                            password=DefaultConfig.ODOO_PASSWORD)

        client.create(model_name="helpdesk.ticket", data_dict={
            "partner_name": "Mitchell Admin",
            "company_id": 1,
            "partner_email": "mitchell.admin@odoo.com",
            "name": '# Customer Report',
            "attachment_ids": False,
            "channel_id": 2,
            "partner_id": 3,
            "user_id": 8,
            "stage_id": 1,
            "team_id": 1,
            "description": json.dumps({
                "type": data.get('type'),

                "oid": data.get('oid'),

                "terminal_id": data.get('terminal_id'),

                "serial_number": data.get('serial_number'),

                "account_id": data.get('account_id'),

                "pos_id": data.get('pos_id'),

                "message": data.get('message'),

                "images": data.get('images')
            }),
        })
        LoggerTask.debug(f'Create new ticket in Odoo{data}')
        pass



    @classmethod
    def run_task(cls, message):
        """
            - The function handle
        """
        # if message.get('key') == ReportEnumKey.REPORT_CREATE:
        cls.create_report(message.get('value'))

        # if message.get('key') == ReportEnumKey.REPORT_SEND_MESS:
        cls.send_report_mess(message.get('value'))

        cls.create_report_in_odoo(message.get('value'))

        LoggerTask.debug(f'run_task {message}')
        pass
