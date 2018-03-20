import os

CONNECTION_MAP = (
    ('db', 'MYSQL_DATABASE'),
    ('user', 'MYSQL_USER'),
    ('password', 'MYSQL_PASSWORD'),
    ('host', 'MYSQL_HOST'),
)


def get_connection():
    return {k: os.environ.get(n) for k, n in CONNECTION_MAP}
