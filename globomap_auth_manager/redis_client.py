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
import json
import logging
from datetime import datetime

import redis
from redis.sentinel import Sentinel

from globomap_auth_manager import settings
from globomap_auth_manager.exceptions import CacheException


class RedisClient(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.sentinel_endpoint_simple = settings.REDIS_SENTINEL_ENDPOINT_SIMPLE
        self.sentinels_port = settings.REDIS_SENTINELS_PORT
        self.sentinels = settings.REDIS_SENTINELS
        self.sentinel_service_name = settings.REDIS_SENTINEL_SERVICE_NAME
        self.sentinel_password = settings.REDIS_SENTINEL_PASSWORD
        self.host = settings.REDIS_HOST
        self.port = settings.REDIS_PORT
        self.password = settings.REDIS_PASSWORD

        self.get_redis_conn()

    def get_redis_conn(self):
        if self.sentinel_endpoint_simple:
            connection = self._get_redis_sentinel_conn()
        else:
            connection = self._get_redis_conn()

        self.conn = connection

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

    def get_cache_token(self, token):
        """ Get token and data from Redis """

        if not self.conn:
            raise CacheException('Redis is not connected')

        token_data = self.conn.get(token)
        token_data = json.loads(token_data) if token_data else None

        return token_data

    def set_cache_token(self, token_data):
        """ Set Token with data in Redis """

        if not self.conn:
            raise CacheException('Redis is not connected')

        token = token_data['token']['id']

        token_expires = token_data['token']['expires']
        datetime_object = datetime.strptime(
            token_expires, '%Y-%m-%dT%H:%M:%SZ')
        ttl = (datetime.utcnow().now() - datetime_object)
        token_data = json.dumps(token_data)

        self.conn.set(token, token_data, ex=ttl.seconds)

    def is_redis_ok(self):
        if not self.conn or not self.conn.ping():
            self.logger.error('Failed to healthcheck redis.')
            return False
        else:
            return True
