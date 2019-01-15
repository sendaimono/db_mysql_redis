# -*- coding: utf-8 -*-
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from chalicelib.common import ENV_VARIABLES
from chalicelib.types import DICT
import logging as log

Base = declarative_base()
ENGINE = 'ENGINE'
SESSION = 'SESSION'

__state: DICT = {}


def __in_state(fun):
    def wrapper():
        key = fun.__name__
        value = __state.get(key)
        if not value:
            log.debug(f'Creating {key}')
            value = fun()
            __state[key] = value
        return value
    return wrapper


@__in_state
def engine():
    from sqlalchemy import create_engine
    log.debug(ENV_VARIABLES.DATABASE_URL)
    return create_engine(ENV_VARIABLES.DATABASE_URL)


@__in_state
def session() -> Session:
    return sessionmaker(bind=engine())
