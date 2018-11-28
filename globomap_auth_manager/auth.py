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

import requests

from globomap_auth_manager import settings
from globomap_auth_manager.exceptions import CacheException
from globomap_auth_manager.exceptions import InvalidToken
from globomap_auth_manager.keystone_auth import KeystoneAuth
from globomap_auth_manager.redis_client import RedisClient


class Auth(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.token = None
        self.token_data = None
        self.cache = None
        self._keystone_auth = None
        self.configure_cache()

    def is_url_ok(self):
        """ Verify Keystone Auth URL """

        response = requests.head(settings.KEYSTONE_AUTH_URL)
        if response.status_code == 200:
            return True
        return False

    def set_credentials(self, username=None, password=None):
        """ Set credentials """

        self._set_config_keystone(username, password)

    def set_token(self, value):
        """ Set Token """

        if value and value.find('Token token=') == 0:
            token = value[12:]
        else:
            token = value
        self.token = token

    def _set_token_data(self):
        """ Set token_data by Keystone """

        if not self.token:
            return

        self._set_config_keystone(
            settings.KEYSTONE_USERNAME, settings.KEYSTONE_PASSWORD)

        token_data = self._keystone_auth.validate_token(self.token)

        if not token_data:
            self.logger.error('Invalid Token')
            raise InvalidToken('Invalid Token')

        self.token_data = token_data

        if self.cache.is_redis_ok():
            try:
                self.cache.set_cache_token(token_data)
            except CacheException:
                self.logger.error('Token not setted in cache.')

    def _set_config_keystone(self, username, password):
        """ Set config to Keystone """

        self._keystone_auth = KeystoneAuth(
            settings.KEYSTONE_AUTH_URL, settings.KEYSTONE_PROJECT_NAME, username, password,
            settings.KEYSTONE_USER_DOMAIN_NAME, settings.KEYSTONE_PROJECT_DOMAIN_NAME,
            settings.KEYSTONE_TIMEOUT)

    def get_token_data(self):
        """ Get token and data from keystone """

        token_data = self._keystone_auth.conn.auth_ref
        token = token_data['auth_token']
        self.set_token(token)

        if self.cache.is_redis_ok():
            try:
                self.cache.set_cache_token(token_data)
            except CacheException:
                self.logger.error('Token not setted in cache.')

        token_data = {
            'expires_at': token_data['expires_at'],
            'token': token
        }

        return token_data

    def validate_token(self):
        """ Validate Token """

        if not self.token:
            self.logger.error('Missing Token')
            raise InvalidToken('Missing Token')

        if self.cache.is_redis_ok():
            try:
                token_data = self.cache.get_cache_token(self.token)
            except CacheException:
                self.logger.error('Token not getted from cache.')
                self._set_token_data()
            else:
                if token_data:
                    self.token_data = token_data
                else:
                    self._set_token_data()
        else:
            self._set_token_data()

    def get_token_data_details(self):
        return self.token_data

    def configure_cache(self):
        if settings.USE_REDIS == '1':
            self.cache = RedisClient()
