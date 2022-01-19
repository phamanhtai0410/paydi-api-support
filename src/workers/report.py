from paydi_lib.logger import LoggerTask
from src.models.report import Report
from src.utils.send__telegram_mess import *
from src.config import DefaultConfig
from src.constants import Constants
import xmlrpc.client


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
        if (data.get('type') == 'transaction'):
            message = '<strong>{}: {} #{} </strong> ' \
                      '<pre>' \
                      '<i>Odoo Contact ID      : " {} "</i> \n' \
                      '<i>Account ID           : " {} "</i> \n' \
                      '<i>Serial Number        : " {} "</i> \n' \
                      '<i>Device ID            : " {} "</i> \n' \
                      '<i>Pos ID               : " {} "</i> \n' \
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
                        data.get('message'))
        else:
            message = '<strong>{}: {} </strong> ' \
                      '<pre>' \
                      '<i>Odoo Contact ID      : " {} "</i> \n' \
                      '<i>Account ID           : " {} "</i> \n' \
                      '<i>Serial Number        : " {} "</i> \n' \
                      '<i>Device ID            : " {} "</i> \n' \
                      '<i>Pos ID               : " {} "</i> \n' \
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
                        data.get('message'))

        result = send_telegram_message(token_id=DefaultConfig.TELE_SUPPORT_TOKEN_ID,
                                       chat_id=DefaultConfig.TELE_SUPPORT_CHAT_ID, message=message)
        LoggerTask.debug(f'send to Tele res = {result}')

    @staticmethod
    def create_report_in_odoo(data):
        LoggerTask.debug(f'Create new ticket in Odoo{data}')

        client = XMLRPC_API(url=DefaultConfig.ODOO_MMS_URL,
                            db=DefaultConfig.ODOO_MMS_DB,
                            username=DefaultConfig.ODOO_MMS_USERNAME,
                            password=DefaultConfig.ODOO_MMS_PASSWORD)

        def get_html_images(images: list) -> str:
            list_images_link = []
            for i in images:
                list_images_link.append(f'<div><a href="{i}">{i}</a></div>')
            return ''.join(list_images_link)

        def get_company_id(odoo_contact_id: str) -> int:
            return client.read(model_name="res.partner", conditions=[('id', '=', int(odoo_contact_id))],
                               params={'fields': ['company_id'], 'limit': 1})[0].get('company_id')

        if data.get('odoo_contact_id'):
            company_id = get_company_id(data.get('odoo_contact_id'))[0]
            LoggerTask.debug(f'--- Get company ID = {company_id}')
        else:
            company_id = 1

        LoggerTask.debug(f'Create report odoo - get company id = {company_id}')
        images = get_html_images(data.get('images'))
        # LoggerTask.debug(f'--- Create Odoo ticket - images: {images}')

        client.create(model_name="helpdesk.ticket", data_dict={
            "partner_name": DefaultConfig.ODOO_TICKET_PARTNER_NAME,
            "partner_id": int(DefaultConfig.ODDO_TICKET_PARTNER_ID),
            "partner_email": DefaultConfig.ODDO_TICKET_PARTNER_EMAIL,
            "name": '# Customer Report',
            "attachment_ids": False,
            "channel_id": 2,
            "company_id": company_id,
            "user_id": 8,
            "stage_id": 1,
            "team_id": int(DefaultConfig.ODOO_TICKET_TEAM_ID),
            "description": f"<div><strong>1. </strong>Type : {Constants.REPORT_TYPE_DICT.get(data.get('type'))}</div> \
                            <div><strong>2. </strong>OID : {data.get('oid') if data.get('oid') != 'app_oid' else 'None'}</div> \
                            <div><strong>3. </strong>Terminal ID : {data.get('terminal_id')}</div> \
                            <div><strong>4. </strong>Serial Number : {data.get('serial_number')}</div> \
                            <div><strong>5. </strong>Account ID : {data.get('account_id')}</div> \
                            <div><strong>6. </strong>POS ID : {data.get('pos_id')}</div> \
                            <div><strong>7. </strong>Message : {data.get('message')}</div> \
                            <div><strong>8. </strong>Images : {images}</div> "
        })

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
