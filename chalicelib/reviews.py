from chalicelib.types import REQUEST, HEADERS, DICT
from chalicelib.validator import authorize_request, validate_request
from chalicelib.common import generate_random_string
from chalicelib.database.db import User, Movie, Session, Review
from chalicelib.movies import find_movie_by_gid
import chalicelib.json_proto as proto
import logging as log
from typing import Sequence


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