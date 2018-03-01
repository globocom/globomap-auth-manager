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

from globomap_auth_manager.exceptions import InvalidToken
from globomap_auth_manager.keystone_auth import KeystoneAuth


class Auth(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.redis = None
        self.token = None

    def set_config_keystone(self, auth_url=None, tenant_name=None, username=None, password=None):
        """ Set config to Keystone """

        self.keystone_auth = KeystoneAuth(
            auth_url, tenant_name, username, password)
        return self.keystone_auth

    def set_config_sentinel(self, sentinel_endpoint_simple, sentinels_port,
                            sentinels, sentinel_service_name,
                            sentinel_password):
        """ Set config to Redis sentinel  """

        self.redis = self.RedisClient()
        self.set_config_sentinel(sentinel_endpoint_simple, sentinels_port,
                                 sentinels, sentinel_service_name,
                                 sentinel_password)

    def set_config(self, host, port, password):
        """ Set config to Redis """

        self.redis = self.RedisClient()
        self.set_config(host, port, password)

    def get_token_data(self):
        """ Get token and data from keystone """

        token = self.keystone_auth.conn.auth_ref['token']
        self._set_cache_token(token)
        return token

    def set_token(self, value):
        """ Set Token in instance """

        if value.find('Token token=') == 0:
            token = value[12:]
        else:
            token = value
        self.token = token

    def validate_token(self):
        """ Validate Token """

        self._is_redis_configured()

        if self.token is not None:
            token_data = self._get_cache_token()
            if not token_data:
                self.logger.error('Invalid Token %s' % self.token)
                raise InvalidToken('Invalid Token')
        else:
            self.logger.error('Invalid Token')
            raise InvalidToken('Invalid Token')

        return token_data

    def _get_cache_token(self):
        """ Get token and data from Redis """

        self._is_redis_configured()

        conn = self.redis.get_redis_conn()
        token_data = conn.get(self.token)
        token_data = json.loads(token_data) if token_data else None

        return token_data

    def _set_cache_token(self, token_data):
        """ Set Token with data in Redis """

        conn = self.redis.get_redis_conn()
        token = token_data['token']['id']
        self.set_token(token)

        token_expires = token_data['token']['expires']
        datetime_object = datetime.strptime(
            token_expires, '%Y-%m-%dT%H:%M:%SZ')
        ttl = (datetime.utcnow().now() - datetime_object)
        token_data = json.dumps(token_data)
        conn.set(token, token_data, ex=ttl.seconds)

    def _is_redis_configured(self):
        if self.redis is None:
            raise Exception('Redis is not configured')
        return True
