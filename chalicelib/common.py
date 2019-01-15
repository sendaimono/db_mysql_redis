import string
import secrets

class ENV_VARIABLES:
    DATABASE_URL = 'postgres://postgres:root@localhost:5433/movie_rental'
    REDIS_URL = 'localhost:6379'


def generate_random_string(length) -> str:
    availables = string.ascii_letters + string.digits
    return ''.join(
        secrets.choice(availables) for i in range(length))