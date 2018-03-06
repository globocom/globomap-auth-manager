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
from globomap_auth_manager.exceptions import AuthException
from globomap_auth_manager.settings import KEYSTONE_AUTH_ENABLE


def is_enable(func):

    def func_wrapper(*args, **kwargs):
        if KEYSTONE_AUTH_ENABLE != '1':
            raise AuthException('Auth is not enabled')
        return func(*args, **kwargs)

    return func_wrapper
