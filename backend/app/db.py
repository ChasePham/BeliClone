# Database access: the only place that knows how to connect to Postgres.
import psycopg
from psycopg.rows import dict_row


DATABASE_URL = "postgresql://chasepham@localhost:5432/Beli"


# Opens a new connection; rows come back as dicts so routes can return them as JSON.
def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)
