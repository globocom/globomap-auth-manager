import os

KEYSTONE_USERNAME = os.getenv('KEYSTONE_USERNAME')
KEYSTONE_PASSWORD = os.getenv('KEYSTONE_PASSWORD')
KEYSTONE_TENANT_NAME = os.getenv('KEYSTONE_TENANT_NAME')
KEYSTONE_AUTH_URL = os.getenv('KEYSTONE_AUTH_URL')
KEYSTONE_AUTH_ENABLE = os.getenv('KEYSTONE_AUTH_ENABLE')

REDIS_SENTINEL_ENDPOINT_SIMPLE = os.getenv('REDIS_SENTINEL_ENDPOINT_SIMPLE')
REDIS_SENTINELS_PORT = os.getenv('REDIS_SENTINELS_PORT')
REDIS_SENTINELS = os.getenv('REDIS_SENTINELS')
REDIS_SENTINEL_SERVICE_NAME = os.getenv('REDIS_SENTINEL_SERVICE_NAME')
REDIS_SENTINEL_PASSWORD = os.getenv('REDIS_SENTINEL_PASSWORD')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')
USE_REDIS = os.getenv('USE_REDIS')