# GloboMap Auth Manager

Python client for GloboMap Auth

## Starting Project:

` make setup `

## Running Tests:

` make setup ` (When project not started yet.)<br>
` make tests `

## Environment variables configuration

All of the environment variables below must be set for the api to work properly.

| Variable                           |  Description                  | Example                       |
|------------------------------------|-------------------------------|-------------------------------|
| KEYSTONE_USERNAME                  | Keystone username             | username                      |
| KEYSTONE_PASSWORD                  | Keystone password             | xyz                           |
| KEYSTONE_PROJECT_NAME              | Keystone project name         | globomap                      |
| KEYSTONE_AUTH_URL                  | Keystone auth url             | http://auth.domain.com/v3     |
| KEYSTONE_USER_DOMAIN_NAME          | keystone user domain name     | default                       |
| KEYSTONE_PROJECT_DOMAIN_NAME       | keystone project domain name  | default                       |

### Using REDIS as cache of Auth (optional)

#### SENTINEL

All of the environment variables below must be set for the to work properly.

| Variable                           |  Description                     | Example                                                               |
|------------------------------------|----------------------------------|-----------------------------------------------------------------------|
| REDIS_SENTINEL_ENDPOINT_SIMPLE     | Control variable to use Sentinel | 1                                                                     |
| REDIS_SENTINELS_PORT               | Redis Sentinel port              | 26379                                                                 |
| REDIS_SENTINELS                    | Redis Sentinel adrress           | auth1.sentinel.domain.com,auth2.sentinel.domain,auth3.sentinel.domain |
| REDIS_SENTINEL_SERVICE_NAME        | Redis Sentinel service name      | service_name                                                          |
| REDIS_SENTINEL_PASSWORD            | Redis Sentinel password          | xyz                                                                   |
| USE_REDIS                          | Control variable to use Redis    | 1                                                                     |

#### REDIS

| Variable                           |  Description                     | Example                      |
|------------------------------------|----------------------------------|------------------------------|
| REDIS_HOST                         | Redis host                       | auth.sentinel.domain.com     |
| REDIS_PORT                         | Redis port                       | 6379                         |
| REDIS_PASSWORD                     | Redis password                   | xyz                          |
| USE_REDIS                          | Control variable to use Redis    | 1                            |


## Licensing

GloboMap Auth Manager is under [Apache 2 License](./LICENSE)
