# -*- coding: utf-8 -*-



# File: send_mess_to_telegram.py
# Created at 16/11/2021
"""
   Description:
        -
        -
"""
import json
import logging
import sys
import traceback
from datetime import datetime

from sentry_sdk import capture_exception

from src.utils.format import json_encode_hook
from inspect import getframeinfo, stack
import requests

def send_telegram_message(token_id, chat_id, message):
    try:
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'HTML'
        }
        return requests.post('https://api.telegram.org/bot{token}/sendMessage'.format(token=token_id), data=payload,
                             verify=False).content
    except Exception as e:
        capture_exception(e)

