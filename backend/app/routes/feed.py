from flask import Blueprint, request

from app.db import get_connection, user_exists

# Blueprint for the feed feature. There's no posts table: the feed is the
# rankings of the users you follow, newest first.

bp = Blueprint('feed', __name__)

DEFAULT_LIMIT = 50
MAX_LIMIT = 100


# Endpoint #7: ranking activity from the users <user_id> follows.
# Optional ?limit= (1-100, default 50).
@bp.get("/users/<int:user_id>/feed")
def get_feed(user_id):
    limit = request.args.get("limit", DEFAULT_LIMIT)
    try:
        limit = int(limit)
    except ValueError:
        return {"error": "limit must be an integer"}, 400
    if limit < 1 or limit > MAX_LIMIT:
        return {"error": f"limit must be between 1 and {MAX_LIMIT}"}, 400

    with get_connection() as conn:
        if not user_exists(conn, user_id):
            return {"error": "user not found"}, 404

        items = conn.execute(
            """
            SELECT u.id AS user_id, u.username, u.display_name,
                   r.id AS restaurant_id, r.name, r.cuisine, r.city,
                   ur.rank_position, ur.created_at
            FROM follows f
            JOIN user_rankings ur ON ur.user_id = f.followee_id
            JOIN users u ON u.id = ur.user_id
            JOIN restaurants r ON r.id = ur.restaurant_id
            WHERE f.follower_id = %s
            ORDER BY ur.created_at DESC, ur.id DESC
            LIMIT %s
            """,
            (user_id, limit),
        ).fetchall()

    return items
