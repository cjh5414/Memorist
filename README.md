# Memorist

## Test  

[![Code Cov Badge](https://codecov.io/gh/cjh5414/Memorist/branch/master/graphs/badge.svg)](https://codecov.io/gh/cjh5414/Memorist/)

- unit test with pytest

## Continuous Integration

- Circe CI
 
## Automatic Deployment

- Circle-ci
- github Webhooks
- scripts

## Error Tracking

- Sentry

## Environment Variables

name |  value | description
---- | ---- | ----
MEMORIST_SECRET_KEY | | Django secret key
MEMORIST_MYSQL_NAME | | MySQL DB name
MEMORIST_MYSQL_USER | | MySQL user name
MEMORIST_MYSQL_PASSWORD | | MySQL user password
SENTRY_KEY | | Sentry key
SENTRY_SECRET | | Sentry secret key(with sentry project number)
MEMORIST_ENVIRONMENT | local(default) | local environment
 　| production | production server environment
PAPAGO_API_CLIENT_ID | | Papago API client ID
PAPAGO_API_CLIENT_SECRET | | Papago API client secret
OXFORD_API_ID | | Oxford API ID 
OXFORD_API_KEY | | Oxford API key


