# -*- coding: utf-8 -*-


# File: pos.py
# Created at 11/11/2021
"""
   Description: 
        -
        -
"""
from src.exceptions.handler import handle_exception
from src.producers.base import send_message_to_topic

"""
    
    Format message:
    
    Topic: "test"
        
        {
            "action": PUT, POST, DELETE
            "value": object
        }
        
        - PUT = Update something
        - POST = Request or submit something
        - DELETE = Remove or delete something
"""


@handle_exception()
def send_task(topic, data):
    send_message_to_topic(topic, {
        'action': "POST",
        "value": data
    })
