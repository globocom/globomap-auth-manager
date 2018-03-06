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

from globomap_auth_manager.exceptions import InvalidToken
from globomap_auth_manager.keystone_auth import KeystoneAuth
from globomap_auth_manager.settings import KEYSTONE_AUTH_URL
from globomap_auth_manager.settings import KEYSTONE_PASSWORD
from globomap_auth_manager.settings import KEYSTONE_TENANT_NAME
from globomap_auth_manager.settings import KEYSTONE_USERNAME


class Auth(object):

    logger = logging.getLogger(__name__)

    def __init__(self):
        self.token = None

    def set_credentials(self, username=None, password=None):
        self._set_config_keystone(username, password)

    def set_token(self, value):
        """ Set Token in instance """

        if value.find('Token token=') == 0:
            token = value[12:]
        else:
            token = value
        self.token = token

    def _set_config_keystone(self, username, password):
        """ Set config to Keystone """

        self._keystone_auth = KeystoneAuth(
            KEYSTONE_AUTH_URL, KEYSTONE_TENANT_NAME, username, password)
        return self._keystone_auth

    def get_token_data(self):
        """ Get token and data from keystone """

        token_data = self._keystone_auth.conn.auth_ref
        return token_data['token']

    def validate_token(self):
        """ Validate Token """

        self._set_config_keystone(KEYSTONE_USERNAME, KEYSTONE_PASSWORD)
        if self.token is not None:
            token_data = self._keystone_auth.validate_token(self.token)
            if not token_data:
                self.logger.error('Invalid Token %s' % self.token)
                raise InvalidToken('Invalid Token')
            token_data = token_data.to_dict()
        else:
            self.logger.error('Invalid Token')
            raise InvalidToken('Invalid Token')

        return token_data
