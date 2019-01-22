import string
import secrets
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime

class ENV_VARIABLES:
    DATABASE_URL = 'postgres://postgres:root@localhost:5433/movie_rental'
    REDIS_URL = 'localhost:6379'


def generate_random_string(length) -> str:
    availables = string.ascii_letters + string.digits
    return ''.join(
        secrets.choice(availables) for i in range(length))

def convert_table_to_dict(obj):
    def conv(val):
        if isinstance(val, datetime):
            return val.isoformat()
        return val
    try:
        columns = obj.__table__.columns
        return {
            c.name: conv(getattr(obj, c.name))
            for c in columns
        }
    except:
        return None