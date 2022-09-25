import os

DB_POOL_CONN = {
    "maxconnections": 5,
    "mincached": 2,
    "maxcached": 3,
    "blocking": True,
    "setsession": [],
    "ping": 0,
    "host": os.getenv("DB_HOST"),
    "port": 3306,
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": 'blog',
    "charset": 'utf8'
}
