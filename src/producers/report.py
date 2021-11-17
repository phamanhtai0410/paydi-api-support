
# File: report.py	
# Created at 16/11/2021
"""
   Description: 
        -
        -
"""
from src.exceptions.handler import handle_exception
from src.producers.base import send_message_to_topic



@handle_exception()
def send_create_report_task(topic: str, value: dict, key: str) -> None:
    send_message_to_topic(topic, {
        'action': 'POST',
        'value': value,
        'key': key
    })

@handle_exception()
def send_push_telegram_report_mess_task(topic: str, value: dict, key: str) -> None:
    send_message_to_topic(topic, {
        'action': 'PUSH_MESS',
        'value': value,
        'key': key
    })