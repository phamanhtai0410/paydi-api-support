# -*- coding: utf-8 -*-


# File: report.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""

from pymodm import fields
from paydi_lib.model import BaseMG

SIZE = 10000


class Report(BaseMG):
    """
        Save general infos of customer
    """

    class Meta:
        collection_name = 'paydi_report'
        final = True

    _id = fields.ObjectIdField(primary_key=True)
    type = fields.CharField(blank=False, default='app_error')
    oid = fields.CharField(blank=True, default='app_oid')
    terminal_id = fields.CharField(blank=True)
    merchant_id = fields.CharField(blank=True)
    serial_number = fields.CharField(blank=True)
    odoo_contact_id = fields.CharField(blank=True)
    account_id = fields.CharField(blank=True)
    pos_id = fields.CharField(blank=True)
    message = fields.CharField(blank=True)
    images = fields.ListField(field=fields.CharField(), blank=True)
