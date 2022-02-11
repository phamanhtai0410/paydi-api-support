# -*- coding: utf-8 -*-



# File: extensions.py
# Created at 03/11/2021
"""
   Description:
        -
        -
"""
from flask_redis import Redis
from apscheduler.schedulers.background import BackgroundScheduler

# Redis cache
from kafka import KafkaProducer
from rediscluster import RedisCluster

from src.config import DefaultConfig

redis_cache = Redis()
# Redis user info, will initialized in app
redis_cluster = RedisCluster(startup_nodes=DefaultConfig.REDIS_CLUSTER,
                             decode_responses=True)

redis_global = RedisCluster(startup_nodes=DefaultConfig.REDIS_GLOBAL,
                            decode_responses=True)

jobs = BackgroundScheduler(daemon=True)
"""
    - Kafka producer
"""
producer = KafkaProducer(bootstrap_servers=DefaultConfig.KAFKA_SERVER)
