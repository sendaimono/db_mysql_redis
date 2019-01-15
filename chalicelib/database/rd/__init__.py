from .database import session
import redis
import json

def Session() -> redis.Redis:
    return session()

def get_reviews_for_movie(gid: str):
    revs: bytes = Session().get(f'review-{gid}')
    if revs is None:
        return None
    decoded = revs.decode()
    return json.loads(decoded)

def del_reviews_for_movie(gid: str):
    return Session().delete(f'review-{gid}')

def check_if_exists_reviews_for_movie(gid: str):
    return Session().exists(f'review-{gid}')

def set_reviews_for_movie(gid: str, reviews):
    return Session().set(f'review-{gid}', json.dumps(reviews))