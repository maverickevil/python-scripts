import pymysql
from dbutils.pooled_db import PooledDB

# TODO
#   you can put the configuration in the settings file.
#   e.g.    from config.settings import DB_POOL_CONN

# Connection pool configuration item
DB_POOL_CONN = {
    'maxconnections': 5,
    'mincached': 2,
    'maxcached': 3,
    'blocking': True,
    'setsession': [],
    'ping': 0,
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'root@123',
    'database': 'testdb',
    'charset': 'utf8'
}


def wrapper_auto(func):
    """
    Automatically connect and close cursor.
    """

    def inner(self, sql, **kwargs):
        # conn, cursor
        args = self.get_conn_cursor()
        res = func(self, sql, *args, **kwargs)
        self.close_conn_cursor(*args)
        return res

    return inner


class Connect(object):
    """
    DB operation tool class.
    """

    def __init__(self):
        self.pool = PooledDB(creator=pymysql, **DB_POOL_CONN)

    def get_conn_cursor(self):
        conn = self.pool.connection()
        dict_cursor = pymysql.cursors.DictCursor
        cursor = conn.cursor(dict_cursor)
        return conn, cursor

    @staticmethod
    def close_conn_cursor(*args):
        for item in args:
            item.close()

    @wrapper_auto
    def exec(self, sql, *args, **kwargs):
        conn, cursor = args
        cursor.execute(sql, kwargs)
        conn.commit()

    @wrapper_auto
    def fetch_one(self, sql, *args, **kwargs):
        conn, cursor = args
        cursor.execute(sql, kwargs)
        result = cursor.fetchone()
        return result

    @wrapper_auto
    def fetch_all(self, sql, *args, **kwargs):
        conn, cursor = args
        cursor.execute(sql, kwargs)
        result = cursor.fetchall()
        return result


# New an object (singleton mode)
db = Connect()


# Example of use
if __name__ == '__main__':
    res = db.fetch_one("select * from table_name")
    print(res)

