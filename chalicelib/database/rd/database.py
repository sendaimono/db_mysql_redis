import redis
from chalicelib.common import ENV_VARIABLES
from chalicelib.types import DICT
import logging as log
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
def session() -> redis.Redis:
    conn = ENV_VARIABLES.REDIS_URL.split(':')
    return redis.Redis(host = conn[0], port=int(conn[1]))

    