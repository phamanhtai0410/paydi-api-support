# -*- coding: utf-8 -*-



# File: controller.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""
from datetime import datetime
from paydi_lib.decorators import handle_response, load_data
from paydi_lib.exceptions import NotFound

from bson import ObjectId
from flask import g

from src.schemas import Example
from src.schemas.example import ExampleResponse
from paydi_lib.logger import Logger


@handle_response(schema=ExampleResponse)
@load_data(Example)
def cl_health_check():
    data = g.data
    Logger.debug("call health_check", data)

    if data:
        raise NotFound

    return {
        '_id': ObjectId(),
        'created_time': datetime.utcnow()
    }

