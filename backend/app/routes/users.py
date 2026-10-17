from flask import Blueprint, request

from app.db import get_connection

# Blueprint for the users feature.

bp = Blueprint('users', __name__)


# Endpoint #1: every user, for the frontend's "current user" switcher.
@bp.get("/users")
def list_users():
    with get_connection() as conn:
        users = conn.execute(
            "SELECT id, username, display_name FROM users ORDER BY id"
        ).fetchall()

    return users


# Endpoint #2: one user by id.
@bp.get("/users/<int:user_id>")
def get_user(user_id):
    with get_connection() as conn:
        user = conn.execute(
            "SELECT id, username, display_name FROM users WHERE id = %s",
            (user_id,),
        ).fetchone()

    if user is None:
        return {"error": "user not found"}, 404
    return user


# Creates a user from a JSON body: {"username": "...", "display_name": "..."}.
# Not in the spec's inventory (users are seeded); added for practice.
@bp.post("/users")
def create_user():
    body = request.get_json(silent=True) or {}
    username = body.get("username")
    display_name = body.get("display_name")

    if not username or not display_name:
        return {"error": "username and display_name are required"}, 400

    with get_connection() as conn:
        taken = conn.execute(
            "SELECT 1 FROM users WHERE username = %s", (username,)
        ).fetchone()
        if taken:
            return {"error": "username already taken"}, 409

        user = conn.execute(
            """
            INSERT INTO users (id, username, display_name, created_at)
            VALUES ((SELECT COALESCE(MAX(id), 0) + 1 FROM users), %s, %s, now())
            RETURNING id, username, display_name
            """,
            (username, display_name),
        ).fetchone()

    return user, 201
