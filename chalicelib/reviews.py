from chalicelib.types import REQUEST, HEADERS, DICT
from chalicelib.validator import authorize_request, validate_request
from chalicelib.common import generate_random_string
from chalicelib.database.db import User, Movie, Session, Review
from chalicelib.movies import find_movie_by_gid
import chalicelib.json_proto as proto
import logging as log
from typing import Sequence, List, Tuple
import chalicelib.database.rd as rd


@authorize_request
def create_review(user: User, request: REQUEST):
    valid, msg = validate_request(request, {
        'content': str,
        'mark': int,
        'movie_gid': str

    })
    if not valid:
        return proto.malformed_request('create_review', msg)
    movie = find_movie_by_gid(request['movie_gid'])
    if not movie:
        return proto.error(404, 'Movie not found')
    review: Review = Review.from_dict(request)
    if not review:
        return proto.error(500, "Couldn't add review to db")
    review.movie = movie.id
    review.author = user.id
    session = Session()
    try:
        session.add(review)
        session.commit()
        # checking if there are reviews stored in redis for given movie
        if rd.check_if_exists_reviews_for_movie(movie.gid):
            # if yes then delete entries
            rd.del_reviews_for_movie(movie.gid)
        return proto.ok()
    except Exception as e:
        session.close()
        log.error(e)
        return proto.internal_error('Error while retrieving users')
    finally:
        session.close()


def list_reviews(headers: HEADERS, query_params: REQUEST):
    if not(query_params and query_params.get('gid')):
        return proto.malformed_request('list_reviews', 'Missing gid query_param')
    movie_gid = query_params.get('gid')

    # checking redis
    reviews = rd.get_reviews_for_movie(movie_gid)
    if reviews:
        log.debug("Polling from redis")
        log.debug(reviews)
        return proto.ok(reviews)

    # doesn't exist, pooling from db
    movie = find_movie_by_gid(movie_gid)
    if not movie:
        return proto.error(404, 'Movie not found')
    session = Session()
    try:
        reviews = session.query(
            User.username,
            Review.created,
            Review.mark,
            Review.content).join(
                Review, User.reviews).filter(Review.movie == movie.id).all()
        converted = _review_to_json(reviews)
        # saving reviews to redis
        rd.set_reviews_for_movie(movie_gid, converted)
        return proto.ok(converted)
    except Exception as e:
        session.close()
        log.error(e)
        return proto.internal_error('Error while retrieving reviews')
    finally:
        session.close()


def _review_to_json(reviews: List[Tuple]) -> List[DICT]:
    converted = []
    if not reviews:
        return converted
    for rev in reviews:
        current = {}
        current['author'] = rev[0]
        current['created'] = rev[1].isoformat()
        current['mark'] = rev[2]
        current['content'] = rev[3]
        converted.append(current)
    return converted
