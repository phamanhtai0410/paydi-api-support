# -*- coding: utf-8 -*-


# File: consumer.py
# Created at 10/11/2021
"""
   Description: 
        - Init kafka consumer
        -
"""

from src.config import DefaultConfig
from paydi_lib.worker import Worker

from src.workers.report import ReportWorker

# Config consumer
"""
    - Config consumer
        [topic.group_id]: ClassHandler
"""
worker_config = {
    'support_topic.report_workers': ReportWorker
}

app = Worker(config=worker_config, app_config=DefaultConfig).run()
