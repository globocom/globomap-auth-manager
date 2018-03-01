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

from globomap_auth_manager.redis import RedisClient

logger = logging.getLogger(__name__)


def _is_redis_ok():
    try:
        conn = RedisClient().get_redis_conn()
    except:
        logger.error('Failed to healthcheck redis.')
        return {'status': False}
    else:
        if not conn.ping():
            logger.error('Failed to healthcheck redis.')
            return {'status': False}
        else:
            return {'status': True}