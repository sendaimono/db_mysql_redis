from .database import session
import redis
import json
import logging as log

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
