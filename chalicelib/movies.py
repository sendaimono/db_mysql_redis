from chalicelib.types import REQUEST, HEADERS, DICT
from chalicelib.validator import authorize_request, validate_request
from chalicelib.common import generate_random_string
from chalicelib.database.db import User, Movie, Session
import chalicelib.json_proto as proto
import logging as log
from typing import Sequence
import chalicelib.database.rd as rd

@authorize_request
def create_movie(user: User, request: REQUEST):
    valid, msg = validate_request(request, {
        'name': str,
        'description': str,
        'premiere_date': str
    })
    if not valid:
        return proto.malformed_request('create_movie', msg)
    movie: Movie = Movie.from_dict(request)
    if not movie:
        return proto.malformed_request('create_movie', 'Parsing failed')
    movie.gid = generate_random_string(8)
    session = Session()
    try:
        session.add(movie)
        session.commit()

        # checking if there are movies stored in redis
        if rd.check_if_movies_list_exists():
            # if yes then delete entries
            rd.del_movies_list()
            
        return proto.ok()
    except Exception as e:
        session.close()
        log.error(e)
        return proto.internal_error('Error while retrieving users')
    finally:
        session.close()


def list_movies():
    # checking redis
    movies = rd.get_movies_list()
    if movies:
        return proto.ok(movies)

    session = Session()
    try:
        movies: Sequence[Movie] = session.query(Movie).all()
        movie_list = [
            movie.to_dict() for movie in movies
        ]
        rd.set_movies_list(movie_list)
        return proto.ok(movie_list)
    except Exception as e:
        session.close()
        log.error(e)
        return proto.internal_error('Error while retrieving users')
    finally:
        session.close()

def find_movie(headers: HEADERS, query_params: REQUEST):
    if not(query_params and query_params.get('gid')):
        return proto.malformed_request('find_movie', 'Missing gid query_param')
    movie_gid = query_params.get('gid')

    # checking redis
    movie = rd.get_movie(movie_gid)
    if movie:
        return proto.ok(movie)

    movie = find_movie_by_gid(movie_gid)
    if movie:
        movie_dct = movie.to_dict(True)
        rd.set_movie(movie_gid, movie_dct)
        return proto.ok(movie_dct)
    return proto.error(404, 'Movie not found')

def find_movie_by_gid(gid: str) -> Movie:
    session = Session()
    try:
        movie: Movie = session.query(Movie).filter_by(
            gid=gid
        ).one_or_none()
        return movie
    except Exception as e:
        session.close()
        log.error(e)
        return None
    finally:
        session.close()
    

