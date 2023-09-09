import json
import os
import logging
from dotenv import dotenv_values


class MetaEnvConfig(type):
    _initiated = False
    _env = {}
    _pg_credentials = {}

    @property
    def env(cls):
        return cls._env

    @env.setter
    def env(cls, env_file:str):
        cls._env = {**os.environ, **dotenv_values(env_file)}

    @property
    def pg_credentials(cls):
        return cls._pg_credentials

    @pg_credentials.setter
    def pg_credentials(cls, env_vars: dict):
        cls._pg_credentials = json.dumps(env_vars.get('PG_CREDENTIALS', '{}'))


class EnvConfig(metaclass=MetaEnvConfig):
    def __new__(cls, env_file:str = '.env'):
        if not cls._initiated:
            logging.info('Initiating charge of environment variables')
            cls.env = env_file
            cls.pg_credentials = cls.env
            logging.debug(f'{cls.env=}')
            logging.debug(f'{cls.pg_credentials=}')


