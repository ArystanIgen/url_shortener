# Standard Library
import logging
from logging.config import dictConfig

import environ

dictConfig(
    config={
        'version': 1,
        'formatters': {
            'f': {
                'format': '{"level": "%(levelname)-4s", "timestamp": "%(asctime)s", '
                          '"module": "%(name)s", "body": "%(message)s"}'
            }
        },
        'handlers': {
            'h': {'class': 'logging.StreamHandler',
                  'formatter': 'f',
                  'level': logging.INFO}
        },
        'root': {
            'handlers': ['h'],
            'level': logging.INFO,
        }
    }
)


@environ.config(prefix='')
class AppConfig:
    @environ.config(prefix="DB")
    class DB:
        username = environ.var()
        password = environ.var()
        host = environ.var()
        port = environ.var(converter=int)
        name = environ.var()
        url = environ.var()
        url_sqlalchemy = environ.var()

    @environ.config(prefix="API")
    class API:
        host = environ.var()
        title = environ.var()
        version = environ.var()
        prefix = environ.var()
        debug = environ.bool_var()
        allowed_hosts = environ.var()

    env = environ.var()

    api: API = environ.group(API)
    db: DB = environ.group(DB)


CONFIG: AppConfig = AppConfig.from_environ()  # type: ignore
