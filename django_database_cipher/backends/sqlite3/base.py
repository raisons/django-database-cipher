import statistics
from django.utils.asyncio import async_unsafe
from django.db.backends.sqlite3.base import DatabaseWrapper as DjangoDatabaseWrapper
from django.db.backends.sqlite3.base import list_aggregate
from django.db.backends.sqlite3.base import FORMAT_QMARK_REGEX

from pysqlcipher3 import dbapi2 as Database

from .utils import get_pragma_key, get_deterministic_params


class SQLiteCursorMixin:

    def execute(self, query, params=None):
        try:
            if params is None:
                return super().execute(query)
            query = self.convert_query(query)
            return super().execute(query, params)
        except Exception as e:
            raise e

    def executemany(self, query, param_list):
        query = self.convert_query(query)
        return super().executemany(query, param_list)

    def convert_query(self, query):
        return FORMAT_QMARK_REGEX.sub('?', query).replace('%%', '%')


class DatabaseWrapper(DjangoDatabaseWrapper):
    Database = Database
    CursorWrapper = SQLiteCursorMixin
    DeterministicParams = get_deterministic_params()

    @async_unsafe
    def get_new_connection(self, conn_params):
        conn = self.Database.connect(**conn_params)
        create_deterministic_function = self.get_create_deterministic_function(conn)

        for params in self.DeterministicParams:
            create_deterministic_function(*params)

        conn.create_aggregate('STDDEV_POP', 1, list_aggregate(statistics.pstdev))
        conn.create_aggregate('STDDEV_SAMP', 1, list_aggregate(statistics.stdev))
        conn.create_aggregate('VAR_POP', 1, list_aggregate(statistics.pvariance))
        conn.create_aggregate('VAR_SAMP', 1, list_aggregate(statistics.variance))
        conn.execute('PRAGMA foreign_keys = ON')
        conn.execute("PRAGMA key='%s';" % get_pragma_key())
        return conn

    def create_cursor(self, name=None):
        return self.connection.cursor(factory=self.get_cursor_factory())

    def get_cursor_factory(self):
        return type('CursorFactory', (self.CursorWrapper, self.Database.Cursor), {})

    def get_create_deterministic_function(self, conn):
        return conn.create_function
