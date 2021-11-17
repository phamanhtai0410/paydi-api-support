# -*- coding: utf-8 -*-



# File: report.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""

from collections import defaultdict
import json
import traceback
from datetime import datetime

import sentry_sdk
from bson import ObjectId
from pymodm import fields
from sentry_sdk import capture_exception
from src.decorators.cache import cache_id, cache_filter
from src.utils.datetime import get_current_time
from src.utils.validators import is_oid
from src.models.base import BaseMG

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
    oid = fields.CharField(blank=False, default='app_oid')
    terminal_id = fields.CharField(blank=True)
    serial_number = fields.CharField(blank=False)
    account_id = fields.CharField(blank=False)
    pos_id = fields.CharField(blank=False)
    message = fields.CharField(blank=True)
    images = fields.ListField(field=fields.CharField(), blank=True)



    
