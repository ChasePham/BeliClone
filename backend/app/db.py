# Database access: the only place that knows how to connect to Postgres.
import os

import psycopg
from dotenv import load_dotenv
from psycopg.rows import dict_row

# Reads DATABASE_URL from backend/.env (git-ignored).
load_dotenv()
DATABASE_URL = os.environ["DATABASE_URL"]


# Opens a new connection; rows come back as dicts so routes can return them as JSON.
# Used as `with get_connection() as conn:` -- everything inside the block is one
# transaction: committed when the block ends, rolled back if an exception is raised.
def get_connection():
    return psycopg.connect(DATABASE_URL, row_factory=dict_row)


# True if a user with this id exists. Shared by routes that are scoped to a user.
def user_exists(conn, user_id):
    row = conn.execute("SELECT 1 FROM users WHERE id = %s", (user_id,)).fetchone()
    return row is not None
