# -*- coding: utf-8 -*-
from chalicelib.types import DATA, RESPONSE, REQUEST, Union  # noqa: F401
from typing import Optional, Any  # noqa: F401
import logging as log


def ok(data: DATA = None) -> RESPONSE:
    if data is not None:
        return {'ok': True, 'data': data}
    return {'ok': True}


def error(code: int, exception: str) -> RESPONSE:
    return {
        'ok': False,
        'error': {
            'code': code,
            'message': str(exception)
        }
    }

def internal_error(e: Union[Exception, str]) -> RESPONSE:
    log.error('Unexpected error: %s' % e)
    return error(500, 'Internal server error.')

def malformed_request(kind, data, cause=None):
    # type: (str, REQUEST, Optional[Any]) -> RESPONSE
    msg = f'Malformed {kind} request'
    caused_by = f'\n\\---> caused by: {cause}' if cause else ''
    log.warning(f'{msg} - ignoring: {data}{caused_by}')
    return error(400, msg)
