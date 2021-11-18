# -*- coding: utf-8 -*-


# File: consumer.py
# Created at 10/11/2021
"""
   Description: 
        - Init kafka consumer
        -
"""
import threading
import time
from functools import wraps

import sentry_sdk
from flask import Flask
from kafka import KafkaConsumer
from pymodm import connect
from sentry_sdk import capture_message
from sentry_sdk.integrations.flask import FlaskIntegration

from src.config import DefaultConfig
from src.utils.format import load_json

# special logs
from src.utils.logger import LoggerTask

from src.workers.simple import Pos
from src.workers.report import ReportWorker

# Config consumer
"""
    - Config consumer
        [topic.group_id]: ClassHandler
"""
worker_config = {
    'test.group_id_1': Pos,
    'support_topic.report_workers': ReportWorker
}


def create_app():
    """Create consumer."""

    configure_extensions()

    return None


def configure_extensions():
    connect(DefaultConfig.MONGODB_URI, connect=False)

    LoggerTask.debug('Connect with MongoDB successfully')

    # Sentry
    if DefaultConfig.SENTRY_DSN:
        sentry_sdk.init(
            dsn=DefaultConfig.SENTRY_DSN,
            integrations=[FlaskIntegration()],
            debug=True,
            server_name=DefaultConfig.PROJECT
        )
        capture_message('{} consumer starts'.format(DefaultConfig.PROJECT))


def create_consumer_app(topic: str, group_id: str):
    create_app()

    _consumer = KafkaConsumer(bootstrap_servers=DefaultConfig.KAFKA_SERVER,
                              auto_offset_reset='earliest',
                              group_id=group_id,
                              consumer_timeout_ms=5000,
                              # enable_auto_commit=False
                              )

    _consumer.subscribe([topic])

    # update transaction: 1 worker
    # 10 g
    LoggerTask.debug('Config.KAFKA_SERVER threading {}'.format(DefaultConfig.KAFKA_SERVER))

    return _consumer


def kafka_consumer(topic: str, group_id: str):
    """
        - Decorator to check and get user info from user token. Return
    """
    _consumer = create_consumer_app(topic, group_id)

    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            decorated_kwargs = {**kwargs, 'consumer': _consumer}
            return f(*args, **decorated_kwargs)

        return wrapper

    return decorator


class Consumer(threading.Thread):

    def __init__(self, topic, group_id, handler):
        threading.Thread.__init__(self)
        self.consumer = create_consumer_app(topic, group_id)

        configure_extensions()
        self.handler = handler

    def run(self) -> None:
        while True:
            for message in self.consumer:
                value = message.value
                json_val = load_json(value)
                LoggerTask.debug(value)

                if value:
                    if hasattr(self.handler, 'run_task'):
                        self.handler.run_task(json_val)
                        self.consumer.commit()


def worker():
    consumers = []
    # app_name = DefaultConfig.PROJECT

    # app = Flask(app_name, instance_relative_config=True)
    for key, value in worker_config.items():
        _key = key.split('.')

        consumer = Consumer(_key[0], _key[1], value)

        consumers.append(consumer)

    LoggerTask.debug('____ consumers ____ {}'.format(len(consumers)))

    # run thread

    for t in consumers:
        t.start()

    while True:
        time.sleep(1)
    return None


app = worker()
