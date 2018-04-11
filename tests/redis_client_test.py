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
from unittest.mock import MagicMock
from unittest.mock import Mock
from unittest.mock import patch

import unittest2

from globomap_auth_manager.redis_client import CacheException
from globomap_auth_manager.redis_client import RedisClient


class RedisClientTest(unittest2.TestCase):

    def tearDown(self):
        patch.stopall()

    def test_get_redis_conn_sentinel(self):

        mock_settings = patch(
            'globomap_auth_manager.redis_client.settings').start()
        mock_sentinel = patch(
            'globomap_auth_manager.redis_client.Sentinel').start()
        mock_redis = patch('globomap_auth_manager.redis_client.redis').start()

        mock_settings.REDIS_SENTINEL_ENDPOINT_SIMPLE = '1'
        mock_settings.REDIS_SENTINELS_PORT = '8000'
        mock_settings.REDIS_SENTINELS = 'localhost1,localhost2,localhost3'
        mock_settings.REDIS_SENTINEL_SERVICE_NAME = 'redis_service'
        mock_settings.REDIS_SENTINEL_PASSWORD = 'password'

        mock_sentinel.return_value.discover_master.return_value = [
            'localhost1', '8000']

        RedisClient()

        mock_sentinel.assert_called_once_with(
            [('localhost1', '8000'), ('localhost2', '8000'), ('localhost3', '8000')],
            socket_timeout=0.1
        )

        mock_redis.StrictRedis.assert_called_once_with(
            host='localhost1', port='8000', password='password'
        )

        mock_sentinel().discover_master.assert_called_once_with('redis_service')

    def test_get_redis_conn_redis(self):

        mock_settings = patch(
            'globomap_auth_manager.redis_client.settings').start()
        mock_redis = patch('globomap_auth_manager.redis_client.redis').start()

        mock_settings.REDIS_SENTINEL_ENDPOINT_SIMPLE = None
        mock_settings.REDIS_HOST = 'localhost'
        mock_settings.REDIS_PORT = '8000'
        mock_settings.REDIS_PASSWORD = 'password'
        RedisClient()

        mock_redis.Redis.assert_called_once_with(
            host='localhost', port='8000', password='password'
        )

    def test_get_cache_token(self):

        mock_settings = patch(
            'globomap_auth_manager.redis_client.settings').start()
        patch('globomap_auth_manager.redis_client.redis').start()

        mock_settings.REDIS_SENTINEL_ENDPOINT_SIMPLE = None
        mock_settings.REDIS_HOST = 'localhost'
        mock_settings.REDIS_PORT = '8000'
        mock_settings.REDIS_PASSWORD = 'password'
        redis_client = RedisClient()

        data = {
            'expires_at': '2018-04-11T19:17:49.870116Z',
            'token': 'token'
        }

        redis_client.conn = Mock()
        redis_client.conn.get.return_value = json.dumps(data)

        self.assertDictEqual(data, redis_client.get_cache_token('123'))

    def test_set_cache_token(self):

        mock_settings = patch(
            'globomap_auth_manager.redis_client.settings').start()
        patch('globomap_auth_manager.redis_client.redis').start()
        mock_datetime = patch(
            'globomap_auth_manager.redis_client.datetime').start()

        mock_settings.REDIS_SENTINEL_ENDPOINT_SIMPLE = None
        mock_settings.REDIS_HOST = 'localhost'
        mock_settings.REDIS_PORT = '8000'
        mock_settings.REDIS_PASSWORD = 'password'
        redis_client = RedisClient()

        mock_datetime.utcnow.return_value.now.return_value.__sub__ = MagicMock(
            return_value=MagicMock(seconds=79802))

        redis_client.conn = Mock()

        redis_client.set_cache_token({
            'expires_at': '2018-04-11T19:17:49.870116Z',
            'auth_token': 'token',
            'roles': [{'name': 'role1', 'id': '123'}]
        })

        token_data = {'expires_at': '2018-04-11T19:17:49.870116Z',
                      'roles': [{'name': 'role1', 'id': '123'}]}

        redis_client.conn.set.assert_called_once_with(
            'token', json.dumps(token_data), ex=79802)

    def test_no_cache_exception(self):

        mock_settings = patch(
            'globomap_auth_manager.redis_client.settings').start()
        patch('globomap_auth_manager.redis_client.redis').start()
        mock_datetime = patch(
            'globomap_auth_manager.redis_client.datetime').start()

        mock_settings.REDIS_SENTINEL_ENDPOINT_SIMPLE = None
        mock_settings.REDIS_HOST = 'localhost'
        mock_settings.REDIS_PORT = '8000'
        mock_settings.REDIS_PASSWORD = 'password'
        redis_client = RedisClient()

        mock_datetime.utcnow.return_value.now.return_value.__sub__ = MagicMock(
            return_value=MagicMock(seconds=79802))

        redis_client.conn = None

        with self.assertRaises(CacheException):
            redis_client.get_cache_token('token')

        with self.assertRaises(CacheException):
            redis_client.set_cache_token('token')
