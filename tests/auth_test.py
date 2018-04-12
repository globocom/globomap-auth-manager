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
from unittest.mock import Mock
from unittest.mock import patch

import unittest2

from globomap_auth_manager import exceptions
from globomap_auth_manager.auth import Auth


class AuthTest(unittest2.TestCase):

    def tearDown(self):
        patch.stopall()

    def test_set_credentials(self):

        mock_settings = patch('globomap_auth_manager.auth.settings').start()
        mock_keystoneauth = patch(
            'globomap_auth_manager.auth.KeystoneAuth').start()

        mock_settings.KEYSTONE_USERNAME = 'username'
        mock_settings.KEYSTONE_PASSWORD = 'password'
        mock_settings.KEYSTONE_PROJECT_NAME = 'project_name'
        mock_settings.KEYSTONE_AUTH_URL = 'auth_url'
        mock_settings.KEYSTONE_AUTH_ENABLE = 'auth_enable'
        mock_settings.KEYSTONE_USER_DOMAIN_NAME = 'user_domain_name'
        mock_settings.KEYSTONE_PROJECT_DOMAIN_NAME = 'project_domain_name'
        Auth().set_credentials('user', 'pass')

        mock_keystoneauth.assert_called_once_with(
            'auth_url', 'project_name', 'user', 'pass',
            'user_domain_name', 'project_domain_name')

    def test_set_token(self):

        auth_inst = Auth()
        auth_inst.set_token('Token token=token123')
        self.assertEqual(auth_inst.token, 'token123')

    def test_get_token_data(self):

        auth_inst = Auth()
        auth_inst.cache = None
        auth_inst._keystone_auth = Mock()
        auth_inst._keystone_auth.conn.auth_ref = {
            'expires_at': '2018-04-11T19:17:49.870116Z',
            'auth_token': 'token',
            'roles': [{'name': 'role1', 'id': '123'}]
        }

        data = {
            'expires_at': '2018-04-11T19:17:49.870116Z',
            'token': 'token'
        }
        auth_inst.token = 'token'
        self.assertEqual(data, auth_inst.get_token_data())

    def test_get_token_data_with_cache(self):

        auth_inst = Auth()
        auth_inst.cache = Mock()
        auth_inst._keystone_auth = Mock()
        auth_ref = {
            'expires_at': '2018-04-11T19:17:49.870116Z',
            'auth_token': 'token',
            'roles': [{'name': 'role1', 'id': '123'}]
        }
        auth_inst._keystone_auth.conn.auth_ref = auth_ref

        data = {
            'expires_at': '2018-04-11T19:17:49.870116Z',
            'token': 'token'
        }
        auth_inst.token = 'token'
        self.assertEqual(data, auth_inst.get_token_data())

        auth_inst.cache.set_cache_token.assert_called_once_with(auth_ref)

    def test_validate_token_with_cache(self):

        auth_inst = Auth()
        auth_inst.cache = Mock()
        auth_inst.cache.get_cache_token.return_value = 'token_data'

        auth_inst.validate_token()
        self.assertEqual('token_data', auth_inst.token_data)

    def test_validate_token(self):

        auth_inst = Auth()
        auth_inst.cache = None
        auth_inst.token = 'token123'
        mock_keystoneauth = patch(
            'globomap_auth_manager.auth.KeystoneAuth').start()

        mock_keystoneauth.return_value.validate_token.return_value = 'token_data'

        auth_inst.validate_token()
        self.assertEqual('token_data', auth_inst.token_data)

    def test_validate_token_with_cache_exception(self):

        auth_inst = Auth()
        auth_inst.cache = Mock()
        auth_inst.cache.get_cache_token.return_value = ''

        with self.assertRaises(exceptions.InvalidToken):
            auth_inst.validate_token()

    def test_validate_token_exception(self):

        auth_inst = Auth()
        auth_inst.cache = None
        mock_keystoneauth = patch(
            'globomap_auth_manager.auth.KeystoneAuth').start()

        mock_keystoneauth.return_value.validate_token.return_value = None

        with self.assertRaises(exceptions.InvalidToken):
            auth_inst.validate_token()
