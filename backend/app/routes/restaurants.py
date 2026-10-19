from flask import Blueprint, request

from app.db import get_connection

# Blueprint for the restaurants feature.

bp = Blueprint('restaurants', __name__)


# Endpoint #3: search restaurants by name, optionally filtered by cuisine and/or city.
# Example: GET /restaurants?q=golden&city=chicago
# All matching is case-insensitive; a missing or empty `q` matches every restaurant.
@bp.get("/restaurants")
def search_restaurants():
    q = request.args.get("q", "")
    cuisine = request.args.get("cuisine")
    city = request.args.get("city")

    # Build the WHERE clause from fixed SQL pieces; values always go in `params`.
    conditions = ["lower(name) LIKE lower(%s)"]
    params = [f"%{q}%"]
    if cuisine:
        conditions.append("lower(cuisine) = lower(%s)")
        params.append(cuisine)
    if city:
        conditions.append("lower(city) = lower(%s)")
        params.append(city)

    sql = (
        "SELECT id, name, cuisine, city, address FROM restaurants WHERE "
        + " AND ".join(conditions)
        + " ORDER BY name, id"
    )

    with get_connection() as conn:
        restaurants = conn.execute(sql, params).fetchall()

    return restaurants


# One restaurant by id.
@bp.get("/restaurants/<int:restaurant_id>")
def get_restaurant(restaurant_id):
    with get_connection() as conn:
        restaurant = conn.execute(
            "SELECT id, name, cuisine, city, address FROM restaurants WHERE id = %s",
            (restaurant_id,),
        ).fetchone()

    if restaurant is None:
        return {"error": "restaurant not found"}, 404
    return restaurant
