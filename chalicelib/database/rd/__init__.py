from .database import session
import redis
import json
import logging as log
from chalicelib.database.db import Review
from chalicelib.common import convert_table_to_dict
import statistics


def Session() -> redis.Redis:
    return session()

###########
# reviews #
###########


def get_reviews_for_movie(gid: str):
    revs: bytes = Session().get(f'review-{gid}')
    if revs is None:
        log.info(f"Didn't find reviews for gid: {gid}")
        return None
    log.info(f"Pulled reviews for movie for gid: {gid}")
    decoded = revs.decode()
    return json.loads(decoded)


def del_reviews_for_movie(gid: str):
    log.info(f"Deleting reviews for movie gid: {gid}")
    return Session().delete(f'review-{gid}')


def check_if_exists_reviews_for_movie(gid: str):
    log.info(f"Checking reviews for movie gid: {gid}")
    return Session().exists(f'review-{gid}')


def set_reviews_for_movie(gid: str, reviews):
    log.info(f"Setting reviews for movie gid: {gid}")
    return Session().set(f'review-{gid}', json.dumps(reviews))


def store_review(review: Review) -> str:
    dct = convert_table_to_dict(review)
    if not dct:
        return None
    log.debug(dct)
    hm_name = f"review:{dct['id']}:raw"
    Session().hmset(hm_name, dct)
    return hm_name


def add_review_to_reviews_store(movie_gid: str, review_rd_id: str):
    Session().rpush(f'reviews:{movie_gid}:raw', review_rd_id)


def get_reviews_list_from_store(movie_gid: str):
    session = Session()
    reviews = session.lrange(f'reviews:{movie_gid}:raw', 0, -1)
    log.debug(reviews)
    if not reviews:
        return None
    scores = []
    for r in reviews:
        log.debug(r)
        res = session.hget(r, 'mark')
        if res is not None:
            scores.append(float(res))
    return statistics.mean(scores)


#########
# movie #
#########


def get_movie(gid: str):
    movie: bytes = Session().get(f'movie-{gid}')
    if movie is None:
        log.info(f"Didn't find movie for gid: {gid}")
        return None
    log.info(f"Pulled movie for gid: {gid}")
    decoded = movie.decode()
    return json.loads(decoded)


def del_movie(gid: str):
    log.info(f"Deleting movie gid: {gid}")
    return Session().delete(f'movie-{gid}')


def check_if_exists_movie(gid: str):
    log.info(f"Checking if movie exists gid: {gid}")
    return Session().exists(f'movie-{gid}')


def set_movie(gid: str, reviews):
    log.info(f"Setting movie gid: {gid}")
    return Session().set(f'movie-{gid}', json.dumps(reviews))


def get_movie_score(gid: str):
    score: bytes = Session().get(f'movie-{gid}-score')
    if score is None:
        log.info(f"Didn't find movie score for gid: {gid}")
        return None
    log.info(f"Pulled movie score for gid: {gid}")
    return float(score)


def del_movie_score(gid: str):
    log.info(f"Deleting movie score gid: {gid}")
    return Session().delete(f'movie-{gid}-score')


def check_if_exists_movie_score(gid: str):
    log.info(f"Checking if movie score exists gid: {gid}")
    return Session().exists(f'movie-{gid}-score')


def set_movie_score(gid: str, score):
    log.info(f"Setting movie score gid: {gid}")
    return Session().set(f'movie-{gid}-score', str(score))


###############
# movies list #
###############

def get_movies_list():
    movies: bytes = Session().get(f'movies-list')
    if movies is None:
        log.info(f"Didn't find movie list")
        return None
    log.info(f"Pulled movie list")
    decoded = movies.decode()
    return json.loads(decoded)


def del_movies_list():
    log.info(f"Deleting movie list")
    return Session().delete(f'movies-list')


def check_if_movies_list_exists():
    log.info(f"Checking if movie list exists")
    return Session().exists(f'movies-list')


def set_movies_list(reviews):
    log.info(f"Setting movie list")
    return Session().set(f'movies-list', json.dumps(reviews))
