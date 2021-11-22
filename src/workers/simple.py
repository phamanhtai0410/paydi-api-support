

# File: simple.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""

from src.utils.logger import LoggerTask

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


class Pos(object):
    # PUT
    @staticmethod
    def update_pos(value):
        print()

    @classmethod
    def run_task(cls, value):
        """
            - The function handle
        """
        if value.get('action') == 'POST':
            cls.update_pos(value.get('value'))

        LoggerTask.debug(f'run_task {value}')
        pass
