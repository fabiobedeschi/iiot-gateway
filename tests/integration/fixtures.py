from subscriber.src.database import Database as SubDatabase
from server.src.database import Database as SerDatabase, Fetch


class Fixtures(SerDatabase, SubDatabase):

    def __init__(self, connection=None, connection_conf=None, keep_retrying=False):
        connection_conf = connection_conf or {
            'user': 'iiot',
            'password': 'lorem',
            'host': 'localhost',
            'port': '5432',
            'dbname': 'iiot',
        }
        super().__init__(connection, connection_conf, keep_retrying)

    def clean_database(self):
        self._execute_query("TRUNCATE TABLE users", fetch=Fetch.NONE)
        self._execute_query("TRUNCATE TABLE waste_bins", fetch=Fetch.NONE)

    def close_connection(self):
        self.connection.close()

    def insert_waste_bin(self, uuid, fill_level, max_level):
        query = f"""
            INSERT INTO waste_bins(uuid, fill_level, max_level, created_at, updated_at)
            VALUES (%s, %s, %s, now(), now())
            RETURNING *
        """
        values = (uuid, fill_level, max_level)
        return self._execute_query(query, values)
