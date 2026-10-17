# Database access: the only place that knows how to connect to Postgres.
import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]


# Opens a new connection; rows come back as dicts so routes can return them as JSON.
def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)
