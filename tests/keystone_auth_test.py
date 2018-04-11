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
from globomap_auth_manager.keystone_auth import KeystoneAuth
from globomap_auth_manager.keystone_auth import NotFound
from globomap_auth_manager.keystone_auth import Unauthorized


class KeystoneAuthTest(unittest2.TestCase):

    def tearDown(self):
        patch.stopall()

    def test_exception_auth_url(self):
        with self.assertRaises(exceptions.AuthException):
            KeystoneAuth(
                project_name='project_name', username='username',
                password='password', user_domain_name='user_domain_name',
                project_domain_name='project_domain_name'
            )

    def test_exception_project_name(self):
        with self.assertRaises(exceptions.AuthException):
            KeystoneAuth(
                auth_url='auth_url', username='username',
                password='password', user_domain_name='user_domain_name',
                project_domain_name='project_domain_name'
            )

    def test_exception_username(self):
        with self.assertRaises(exceptions.AuthException):
            KeystoneAuth(
                auth_url='auth_url', project_name='project_name',
                password='password', user_domain_name='user_domain_name',
                project_domain_name='project_domain_name'
            )

    def test_exception_password(self):
        with self.assertRaises(exceptions.AuthException):
            KeystoneAuth(
                auth_url='auth_url', project_name='project_name',
                username='username', user_domain_name='user_domain_name',
                project_domain_name='project_domain_name'
            )

    def test_exception_user_domain_name(self):
        with self.assertRaises(exceptions.AuthException):
            KeystoneAuth(
                auth_url='auth_url', project_name='project_name',
                username='username', password='password',
                project_domain_name='project_domain_name'
            )

    def test_exception_project_domain_name(self):
        with self.assertRaises(exceptions.AuthException):
            KeystoneAuth(
                auth_url='auth_url', project_name='project_name',
                username='username', password='password',
                user_domain_name='user_domain_name',
            )

    def test_unauthorized(self):
        client_mock = patch(
            'globomap_auth_manager.keystone_auth.client').start()
        client_mock.Client = Mock(side_effect=Unauthorized())

        with self.assertRaises(exceptions.Unauthorized):

            KeystoneAuth(
                auth_url='auth_url', project_name='project_name', username='username',
                password='password', user_domain_name='user_domain_name',
                project_domain_name='project_domain_name'
            )

    def test_token_notfound(self):
        client_mock = patch(
            'globomap_auth_manager.keystone_auth.client').start()
        client_mock.Client = Mock()
        client_mock.Client.return_value.tokens.validate.side_effect = NotFound()

        keystone = KeystoneAuth(
            auth_url='auth_url', project_name='project_name', username='username',
            password='password', user_domain_name='user_domain_name',
            project_domain_name='project_domain_name'
        )
        with self.assertRaises(exceptions.InvalidToken):
            keystone.validate_token('token')

    def test_token_exception(self):
        client_mock = patch(
            'globomap_auth_manager.keystone_auth.client').start()
        client_mock.Client = Mock()
        client_mock.Client.return_value.tokens.validate = Mock(
            side_effect=Exception())

        keystone = KeystoneAuth(
            auth_url='auth_url', project_name='project_name', username='username',
            password='password', user_domain_name='user_domain_name',
            project_domain_name='project_domain_name'
        )
        with self.assertRaises(exceptions.AuthException):
            keystone.validate_token('token')

    def test_validate_token(self):
        client_mock = patch(
            'globomap_auth_manager.keystone_auth.client').start()
        client_mock.Client = Mock()
        client_mock.Client.return_value.tokens.validate.return_value = 'token123'

        keystone = KeystoneAuth(
            auth_url='auth_url', project_name='project_name', username='username',
            password='password', user_domain_name='user_domain_name',
            project_domain_name='project_domain_name'
        )
        data = keystone.validate_token('token')

        self.assertEqual(data, 'token123')
