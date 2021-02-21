from logging import getLogger
from os import getenv

from psycopg2 import connect, Error
from psycopg2.extras import RealDictCursor, RealDictRow

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

    def _open_cursor(self):
        self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)

    def _close_cursor(self):
        if self.cursor:
            self.cursor.close()

    def _commit(self):
        self._close_cursor()
        self.connection.commit()

    def _rollback(self):
        self._close_cursor()
        self.connection.rollback()

    def _execute_query(self, sql, values=None, fetch_all=False):
        self._open_cursor()
        try:
            self.cursor.execute(sql, values)
            result = self.cursor.fetchall() if fetch_all else self.cursor.fetchone()
            self._commit()
            return result

        except Error as e:
            logger.exception(f'Failed to execute query "{sql}" with values "{values}"')
            self._rollback()
            raise e

    def find_all_users(self) -> [RealDictRow]:
        sql = '''
            SELECT * FROM users
        '''
        return self._execute_query(sql, fetch_all=True)

    def find_user(self, uuid) -> RealDictRow:
        sql = '''
            SELECT * FROM users
            WHERE uuid = %(uuid)s
        '''
        values = {'uuid': uuid}
        return self._execute_query(sql, values)

    def update_user(self, uuid, delta) -> RealDictRow:
        sql = '''
            UPDATE users
            SET delta = delta + %(delta)s, updated_at = NOW()
            WHERE uuid = %(uuid)s
            RETURNING *
        '''
        values = {
            'uuid': uuid,
            'delta': delta
        }
        return self._execute_query(sql, values)

    def update_waste_bin(self, uuid, fill_level) -> RealDictRow:
        sql = '''
            UPDATE waste_bins
            SET fill_level = %(fill_level)s, updated_at = NOW()
            WHERE uuid = %(uuid)s
            RETURNING *
        '''
        values = {
            'uuid': uuid,
            'fill_level': fill_level
        }
        return self._execute_query(sql, values)

    # TODO: remove this before delivery
    def insert_user(self, uuid, delta=0) -> RealDictRow:
        sql = '''
            INSERT INTO users (uuid, delta)
            VALUES (%(uuid)s, %(delta)s)
            RETURNING *
        '''
        values = {
            'uuid': uuid,
            'delta': delta
        }
        return self._execute_query(sql, values)

    # TODO: remove this before delivery
    def delete_user(self, uuid) -> RealDictRow:
        sql = '''
            DELETE FROM users
            WHERE uuid = %(uuid)s
            RETURNING *
        '''
        values = {'uuid': uuid}
        return self._execute_query(sql, values)
