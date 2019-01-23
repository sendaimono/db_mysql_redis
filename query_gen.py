from chalicelib.common import generate_random_string as gn
from random import randint

users_count = 1
movies_count = 1
reviews_count = 20000


def create_user():
    return f"INSERT into users (username, login, password) values ('{gn(8)}', '{gn(8)}', '{gn(8)}');"


def create_movies():
    return f"INSERT into movies (gid, name, description, premiere_date) values ('{gn(8)}', '{gn(15)}', '{gn(100)}', NOW());"


def create_review():
    return f"INSERT into reviews (content, movie, created, mark, author) values ('{gn(50)}', {randint(1, movies_count)}, NOW(), {randint(1,10)}, {randint(1, users_count)});"


def reset_idx():
    idx = 'ALTER SEQUENCE users_id_seq RESTART WITH 1;\n'
    idx += 'ALTER SEQUENCE movies_id_seq RESTART WITH 1;\n'
    idx += 'ALTER SEQUENCE reviews_id_seq RESTART WITH 1;'
    return idx


def delete_all():
    idx = 'DELETE FROM reviews;\n'
    idx += 'DELETE FROM movies;\n'
    idx += 'DELETE FROM sessions;\n'
    idx += 'DELETE FROM users;'
    return idx


if __name__ == "__main__":
    with open(f'query_{reviews_count}.sql', 'w') as f:
        f.write(delete_all() + '\n')
        f.write('\n')
        f.write(reset_idx() + '\n')
        f.write('\n')
        for _ in range(users_count):
            f.write(create_user() + '\n')
        f.write('\n')
        for _ in range(movies_count):
            f.write(create_movies() + '\n')
        f.write('\n')
        for _ in range(reviews_count):
            f.write(create_review() + '\n')
