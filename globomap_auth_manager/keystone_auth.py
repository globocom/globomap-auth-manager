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

from keystoneauth1.exceptions.http import NotFound
from keystoneauth1.exceptions.http import Unauthorized
from keystoneclient.v3 import client as client

from globomap_auth_manager import exceptions


class KeystoneAuth(object):

    logger = logging.getLogger(__name__)

    def __init__(self, auth_url=None, tenant_name=None, username=None,
                 password=None, user_domain_name=None,
                 project_domain_name=None):

        if tenant_name is None:
            msg = 'Auth not working. KEYSTONE_TENANT_NAME is not setted.'
            self.logger.exception(msg)
            raise exceptions.AuthException(msg)

        if username is None:
            msg = 'Auth not working. Username is not setted.'
            self.logger.exception(msg)
            raise exceptions.AuthException(msg)

        if password is None:
            msg = 'Auth not working. Password is not setted.'
            self.logger.exception(msg)
            raise exceptions.AuthException(msg)

        if auth_url is None:
            msg = 'Auth not working. KEYSTONE_AUTH_URL is not setted.'
            self.logger.exception(msg)
            raise exceptions.AuthException(msg)

        if user_domain_name is None:
            msg = 'Auth not working. KEYSTONE_USER_DOMAIN_NAME is not setted.'
            self.logger.exception(msg)
            raise exceptions.AuthException(msg)

        if project_domain_name is None:
            msg = 'Auth not working. KEYSTONE_PROJECT_DOMAIN_NAME is not setted.'
            self.logger.exception(msg)
            raise exceptions.AuthException(msg)

        try:
            self.conn = client.Client(
                insecure=True,
                username=username,
                password=password,
                project_name=tenant_name,
                auth_url=auth_url,
                user_domain_name=user_domain_name,
                project_domain_name=project_domain_name,
                timeout=3
            )

        except Unauthorized:
            raise exceptions.Unauthorized('Unauthorized')

    def validate_token(self, token):

        try:
            return self.conn.tokens.validate(token=token)
        except NotFound:
            self.logger.error('Cannot validate token %s' % token)
            raise exceptions.InvalidToken('Invalid Token')
        except:
            raise exceptions.AuthException('Error to validate token')
