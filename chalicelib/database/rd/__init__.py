from .database import session
import redis
def Session() -> redis.Redis:
    return session()