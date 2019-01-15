from chalicelib.types import REQUEST, HEADERS, DICT
from chalicelib.validator import authorize_request, validate_request
from chalicelib.common import generate_random_string
from chalicelib.database.db import User, Movie, Session, Review
from chalicelib.movies import find_movie_by_gid
import chalicelib.json_proto as proto
import logging as log
from typing import Sequence, List, Tuple


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
    movie = find_movie_by_gid(query_params.get('gid'))
    session = Session()
    try:
        reviews = session.query(
            User.username,
            Review.created,
            Review.mark,
            Review.content).join(
                Review, User.reviews).filter(Review.movie == movie.id).all()
        return proto.ok(_review_to_json(reviews))
    except Exception as e:
        session.close()
        log.error(e)
        return proto.internal_error('Error while retrieving users')
    finally:
        session.close()
    if movie:
        return proto.ok(movie.to_dict(True))
    return proto.error(404, 'Movie not found')


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