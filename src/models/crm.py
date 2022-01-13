# -*- coding: utf-8 -*-



# File: report.py
# Created at 16/11/2021
"""
   Description:
        -
        -This model saved infos of CRMs of each companies in system, help MMS controll connection to these CRMs.
"""

from pymodm import fields
from src.models.base import BaseMG

SIZE = 10000

class CRM(BaseMG):
    """
        Save general infos of ccompany: code, crm_url,..etc
    """

    class Meta:
        collection_name = 'crm'
        final = True
    
    _id = fields.ObjectIdField(primary_key=True)
    company_code = fields.CharField(blank=False)
    crm_url = fields.CharField(blank=False)

    
