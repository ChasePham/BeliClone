from flask import Blueprint, request

from app.db import get_connection, user_exists

# Blueprint for the follows feature. Follows are one-directional:
# A following B says nothing about whether B follows A.

bp = Blueprint('follows', __name__)


# Endpoint #5: the users that <user_id> follows.
@bp.get("/users/<int:user_id>/following")
def list_following(user_id):
    with get_connection() as conn:
        if not user_exists(conn, user_id):
            return {"error": "user not found"}, 404

        users = conn.execute(
            """
            SELECT u.id, u.username, u.display_name
            FROM follows f
            JOIN users u ON u.id = f.followee_id
            WHERE f.follower_id = %s
            ORDER BY u.username
            """,
            (user_id,),
        ).fetchall()

    return users


# Endpoint #6: the users who follow <user_id>.
@bp.get("/users/<int:user_id>/followers")
def list_followers(user_id):
    with get_connection() as conn:
        if not user_exists(conn, user_id):
            return {"error": "user not found"}, 404

        users = conn.execute(
            """
            SELECT u.id, u.username, u.display_name
            FROM follows f
            JOIN users u ON u.id = f.follower_id
            WHERE f.followee_id = %s
            ORDER BY u.username
            """,
            (user_id,),
        ).fetchall()

    return users


# Endpoint #8: <user_id> follows someone. Body: {"followee_id": 5}
@bp.post("/users/<int:user_id>/following")
def follow(user_id):
    body = request.get_json(silent=True) or {}
    followee_id = body.get("followee_id")

    # bool is a subclass of int in Python, so rule it out explicitly.
    if type(followee_id) is not int:
        return {"error": "followee_id must be an integer"}, 400
    if followee_id == user_id:
        return {"error": "users can't follow themselves"}, 400

    with get_connection() as conn:
        if not user_exists(conn, user_id) or not user_exists(conn, followee_id):
            return {"error": "user not found"}, 404

        already_following = conn.execute(
            "SELECT 1 FROM follows WHERE follower_id = %s AND followee_id = %s",
            (user_id, followee_id),
        ).fetchone()
        if already_following:
            return {"error": "already following this user"}, 409

        new_follow = conn.execute(
            """
            INSERT INTO follows (follower_id, followee_id, created_at)
            VALUES (%s, %s, now())
            RETURNING follower_id, followee_id, created_at
            """,
            (user_id, followee_id),
        ).fetchone()

    return new_follow, 201


# Endpoint #9: <user_id> unfollows <followee_id>.
@bp.delete("/users/<int:user_id>/following/<int:followee_id>")
def unfollow(user_id, followee_id):
    with get_connection() as conn:
        removed = conn.execute(
            """
            DELETE FROM follows
            WHERE follower_id = %s AND followee_id = %s
            RETURNING follower_id
            """,
            (user_id, followee_id),
        ).fetchone()

    if removed is None:
        return {"error": "not following this user"}, 404
    return "", 204
