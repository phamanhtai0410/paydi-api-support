# -*- coding: utf-8 -*-



# File: datetime.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from datetime import datetime


def get_current_time():
    return datetime.utcnow()


def get_expired_time(start: datetime, time: float):
    return datetime.fromtimestamp(
        start.timestamp() + time
    )
