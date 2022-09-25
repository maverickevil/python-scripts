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


class Connect(object):
    """
    DB operation tool class.
    """

    def __init__(self):
        self.conn = conn = PooledDB(creator=pymysql, **DB_POOL_CONN).connection()
        self.cursor = conn.cursor(pymysql.cursors.DictCursor)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cursor.close()
        self.conn.close()

    def exec(self, sql, *args, **kwargs):
        params = args or kwargs
        # Number of rows affected by executing SQL
        row = self.cursor.execute(sql, params)
        self.conn.commit()
        return row

    def fetch_one(self, sql, *args, **kwargs):
        params = args or kwargs
        self.cursor.execute(sql, params)
        result = self.cursor.fetchone()
        return result

    def fetch_all(self, sql, *args, **kwargs):
        params = args or kwargs
        self.cursor.execute(sql, params)
        result = self.cursor.fetchall()
        return result


# Example of use
if __name__ == '__main__':
    with Connect() as conn:
        sql1 = "select id, nickname from account where username=%s and password=%s"
        res1 = conn.fetch_one(sql1, 'ZhangSan', '12345')
        sql2 = "select id, nickname from account where username=%(username)s and password=%(password)s"
        res2 = conn.fetch_one(sql2, username='LiMing', password='abcde')
        print(res1, res2)

