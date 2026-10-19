from flask import Blueprint, request

from app.db import get_connection, user_exists

# Blueprint for the rankings feature (a user's ranked "been" list).

bp = Blueprint('rankings', __name__)


# Endpoint #4: a user's list, favorite first.
# `score` is calculated from position (10 * (n - position + 1) / n) and never stored.
@bp.get("/users/<int:user_id>/rankings")
def get_rankings(user_id):
    with get_connection() as conn:
        if not user_exists(conn, user_id):
            return {"error": "user not found"}, 404

        rankings = conn.execute(
            """
            SELECT ur.rank_position,
                   ROUND(10.0 * (COUNT(*) OVER () - ur.rank_position + 1)
                         / COUNT(*) OVER (), 1)::float AS score,
                   ur.created_at,
                   r.id AS restaurant_id, r.name, r.cuisine, r.city
            FROM user_rankings ur
            JOIN restaurants r ON r.id = ur.restaurant_id
            WHERE ur.user_id = %s
            ORDER BY ur.rank_position
            """,
            (user_id,),
        ).fetchall()

    return rankings


# Endpoint #10: commit a restaurant at its final position.
# The frontend runs the binary-search comparisons and sends the result:
#   {"restaurant_id": 3, "rank_position": 2}   (1-based; 1..n+1 is valid)
# Shifting the existing rows and inserting the new one happen in one transaction.
@bp.post("/users/<int:user_id>/rankings")
def add_ranking(user_id):
    body = request.get_json(silent=True) or {}
    restaurant_id = body.get("restaurant_id")
    position = body.get("rank_position")

    # bool is a subclass of int in Python, so rule it out explicitly.
    if type(restaurant_id) is not int or type(position) is not int:
        return {"error": "restaurant_id and rank_position must be integers"}, 400

    with get_connection() as conn:
        if not user_exists(conn, user_id):
            return {"error": "user not found"}, 404

        restaurant = conn.execute(
            "SELECT 1 FROM restaurants WHERE id = %s", (restaurant_id,)
        ).fetchone()
        if restaurant is None:
            return {"error": "restaurant not found"}, 404

        already_ranked = conn.execute(
            "SELECT 1 FROM user_rankings WHERE user_id = %s AND restaurant_id = %s",
            (user_id, restaurant_id),
        ).fetchone()
        if already_ranked:
            return {"error": "restaurant is already on this user's list"}, 409

        n = conn.execute(
            "SELECT COUNT(*) AS n FROM user_rankings WHERE user_id = %s", (user_id,)
        ).fetchone()["n"]
        if position < 1 or position > n + 1:
            return {"error": f"rank_position must be between 1 and {n + 1}"}, 400

        # Make room: everything at or below the new spot moves down one.
        conn.execute(
            """
            UPDATE user_rankings SET rank_position = rank_position + 1
            WHERE user_id = %s AND rank_position >= %s
            """,
            (user_id, position),
        )

        ranking = conn.execute(
            """
            INSERT INTO user_rankings (id, user_id, restaurant_id, rank_position, created_at)
            VALUES ((SELECT COALESCE(MAX(id), 0) + 1 FROM user_rankings), %s, %s, %s, now())
            RETURNING id, user_id, restaurant_id, rank_position, created_at
            """,
            (user_id, restaurant_id, position),
        ).fetchone()

    return ranking, 201


# Endpoint #11: remove a restaurant from a user's list.
# Deleting the row and closing the gap happen in one transaction.
@bp.delete("/users/<int:user_id>/rankings/<int:restaurant_id>")
def remove_ranking(user_id, restaurant_id):
    with get_connection() as conn:
        removed = conn.execute(
            """
            DELETE FROM user_rankings
            WHERE user_id = %s AND restaurant_id = %s
            RETURNING rank_position
            """,
            (user_id, restaurant_id),
        ).fetchone()
        if removed is None:
            return {"error": "restaurant is not on this user's list"}, 404

        # Close the gap: everything below the removed spot moves up one.
        conn.execute(
            """
            UPDATE user_rankings SET rank_position = rank_position - 1
            WHERE user_id = %s AND rank_position > %s
            """,
            (user_id, removed["rank_position"]),
        )

    return "", 204
