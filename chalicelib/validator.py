from chalicelib.types import REQUEST, VALIDATORS, HEADERS, VALIDATOR_RES
from chalicelib.database.db import Session, User, UserSession
import logging as log
import chalicelib.json_proto as proto


def authorize(headers: HEADERS):
    token = headers.get('authorization')
    if not token:
        return None
    session = Session()
    try:
        user_session: UserSession = session.query(UserSession).filter_by(
            session_key=token).one_or_none()
        if not user_session: return None
        user: User = session.query(User).filter_by(
            id=user_session.id).one_or_none()
        return user
    except Exception as e:
        log.error(e)
        return None
    finally:
        session.close()

def authorize_request(fun):
    def wrapper(*args, **kwargs):
        args = list(args)
        user: User = authorize(args[0])
        if not user:
            return proto.error(403, "Unknown user")
        args.pop(0)
        args.insert(0, user)
        return fun(*args, **kwargs)
    return wrapper

def validate_request(request: REQUEST, validators: VALIDATORS) -> VALIDATOR_RES:
    for k, t in validators.items():
        val = request.get(k)
        if val:
            if not isinstance(val, t):
                return (False, f'Invalid property {k}')
        else:
            return (False, f'Missing property {k}')
    return (True, None)