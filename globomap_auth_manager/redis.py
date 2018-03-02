# -*- coding: utf-8 -*-
"""
   Copyright 2018 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import logging

import redis
from redis.sentinel import Sentinel


class RedisClient(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.sentinel_endpoint_simple = None

    def set_config_sentinel(self, sentinel_endpoint_simple, sentinels_port,
                            sentinels, sentinel_service_name,
                            sentinel_password):
        self.sentinel_endpoint_simple = sentinel_endpoint_simple
        self.sentinels_port = sentinels_port
        self.sentinels = sentinels
        self.sentinel_service_name = sentinel_service_name
        self.sentinel_password = sentinel_password

    def set_config(self, host, port, password):
        self.host = host
        self.port = port
        self.password = password

    def get_redis_conn(self):
        if self.sentinel_endpoint_simple:
            connection = self._get_redis_sentinel_conn()
        else:
            connection = self._get_redis_conn()

        return connection

    def _get_redis_sentinel_conn(self):
        redis_sentinels = [(rs, self.sentinels_port)
                           for rs in self.sentinels.split(',')]
        redis_service = self.sentinel_service_name
        redis_password = self.sentinel_password
        try:
            sentinel = Sentinel(redis_sentinels, socket_timeout=0.1)
            master = sentinel.discover_master(redis_service)
            connection = redis.StrictRedis(
                host=master[0], port=master[1], password=redis_password)
        except:
            self.logger.exception('Failed to connect to Redis')
            connection = None

        return connection

    def _get_redis_conn(self):
        try:
            connection = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.password
            )
        except:
            self.logger.exception('Failed to connect to Redis')
            connection = None

        return connection

    def is_redis_ok(self):
        try:
            conn = self.get_redis_conn()
        except:
            self.logger.error('Failed to healthcheck redis.')
            return False
        else:
            if not conn or not conn.ping():
                self.logger.error('Failed to healthcheck redis.')
                return False
            else:
                return True
