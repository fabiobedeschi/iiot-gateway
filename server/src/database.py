from logging import getLogger
from os import getenv
from psycopg2 import connect, Error

logger = getLogger()


class Database:
    def __init__(self, connection=None, connection_conf=None):
        self.connection = connection or Database._init_connection(connection_conf)
        self.cursor = None

    @staticmethod
    def _init_connection(connection_conf):
        connection_conf = connection_conf or {
            'user': getenv('POSTGRES_USER'),
            'password': getenv('POSTGRES_PASSWORD'),
            'host': getenv('POSTGRES_HOST'),
            'port': getenv('POSTGRES_PORT'),
            'dbname': getenv('POSTGRES_DB'),
        }
        return connect(**connection_conf)

    def open_cursor(self):
        self.cursor = self.connection.cursor()

    def close_cursor(self):
        if self.cursor:
            self.cursor.close()

    def commit(self):
        self.close_cursor()
        self.connection.commit()

    def rollback(self):
        self.close_cursor()
        self.connection.rollback()

    def execute_query(self, sql, values=None, fetch_all=False):
        self.open_cursor()
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall() if fetch_all else self.cursor.fetchone()
            self.commit()
            return result

        except Error as e:
            logger.exception(f'Failed to execute query "{sql}" with values "{values}"')
            self.rollback()
            raise e

    def find_user(self, uuid):
        sql = '''
            SELECT * FROM users
            WHERE uuid = %(uuid)s
        '''
        values = {'uuid': uuid}
        return self.execute_query(sql, values)

    def update_user(self, uuid, delta):
        sql = '''
            UPDATE users
            SET delta = delta + %(delta)s, updated_at = NOW()
            WHERE uuid = %(uuid)s
            RETURNING uuid
        '''
        values = {
            'uuid': uuid,
            'delta': delta
        }
        return self.execute_query(sql, values)

    def update_waste_bin(self, uuid, fill_level):
        sql = '''
            UPDATE waste_bins
            SET fill_level = %(fill_level)s, updated_at = NOW()
            WHERE uuid = %(uuid)s
            RETURNING uuid
        '''
        values = {
            'uuid': uuid,
            'fill_level': fill_level
        }
        return self.execute_query(sql, values)

    # TODO: remove this before delivery
    def insert_user(self, uuid, delta=0):
        sql = '''
            INSERT INTO users (uuid, delta)
            VALUES (%(uuid)s, %(delta)s)
            RETURNING uuid
        '''
        values = {
            'uuid': uuid,
            'delta': delta
        }
        return self.execute_query(sql, values)

    # TODO: remove this before delivery
    def delete_user(self, uuid):
        sql = '''
            DELETE FROM users
            WHERE uuid = %(uuid)s
            RETURNING uuid
        '''
        values = {'uuid': uuid}
        return self.execute_query(sql, values)
