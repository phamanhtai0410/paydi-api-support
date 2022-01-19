# File: report.py
# Created at 16/11/2021
"""
   Description: 
        -
        -
"""
from paydi_lib.exceptions import handle_exception
from paydi_lib.worker import send_worker


@handle_exception()
def send_create_report_task(topic: str, value: dict, key: str) -> None:
    send_worker(topic, {
        'action': 'POST',
        'value': value,
        'key': key
    })

# @handle_exception()
# def send_push_telegram_report_mess_task(topic: str, value: dict, key: str) -> None:
#     send_message_to_topic(topic, {
#         'action': 'POST',
#         'value': value,
#         'key': key
#     })
