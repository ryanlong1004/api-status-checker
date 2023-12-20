"""
pip install psycopg2-binary sqlalchemy pandas
"""

from typing import Iterable
from sqlalchemy import create_engine
import psycopg2
import pandas as pd


class DbPG:
    def __init__(self):
        # reading
        self.engine = create_engine("postgresql://user:password@server:port/database")

        # writing
        self.conn = psycopg2.connect(
            host="hostname",  # your host, usually localhost
            user="username",  # your username
            password="XXXXXX",  # your password
            database="database/schema",  # required for PostgreSQQ
        )

    def _query(self, query) -> Iterable[tuple]:
        """executes and returns query results as an iterable of tuples"""
        return (item for item in pd.read_sql_query(query, con=self.engine).itertuples(index=False))
