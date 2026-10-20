# Proposal

## Why

The Flask backend has a Blueprint for each feature, but only the users routes are implemented. Restaurants, rankings, follows, and feed are still TODO stubs. The React frontend can't search, rank, follow, or show a feed until those routes read from and write to Postgres correctly. Ranking changes need the most care, because the app (not the schema) has to keep `rank_position` values contiguous.

## What Changes

- Add **restaurant search** (by name, optionally filtered by cuisine and/or city) and a single-restaurant lookup.
- Add **"been" list routes**: get a user's ranked list (with a derived 0–10 score), commit a new restaurant at a final position chosen by the frontend's binary-search loop, and remove a restaurant. Inserts and removes shift the other rows in a single transaction.
- Add **follow routes**: list who a user follows, list a user's followers, follow, and unfollow (one-directional, with no self-follows or duplicates).
- Add a **feed route**: recent ranking activity from the users someone follows, newest first.
- Record the existing **users routes** (list, get, create) as a spec so the API is fully documented.
- Fix supporting backend issues the new routes depend on:
  - `routes/feed.py` currently defines no `bp`, so `app/main.py` fails on import.
  - `app/db.py` hardcodes the database URL instead of reading `DATABASE_URL` from `.env`.
- Every response is JSON. Errors use `{"error": "..."}` with 400 / 404 / 409 status codes.

No breaking changes. The existing `/users` endpoints keep their current behavior.

## Capabilities

### New Capabilities
- `users`: listing, fetching, and creating users. This records behavior that is already implemented.
- `restaurant-search`: finding restaurants by name with optional cuisine/city filters, and fetching one restaurant.
- `been-rankings`: a user's ranked "been" list, plus adding and removing entries while keeping positions contiguous.
- `follows`: one-directional follow relationships, with following/followers lists and follow/unfollow.
- `activity-feed`: ranking activity from followed users, newest first.

### Modified Capabilities
_None. `openspec/specs/` is currently empty._

## Impact

- **Code**: `backend/app/routes/{restaurants,rankings,follows,feed}.py` (new handlers), `backend/app/db.py` (load the URL from `.env`), `backend/app/routes/feed.py` (restore `bp`). No schema changes.
- **APIs**: about 10 new HTTP endpoints under `/restaurants` and `/users/<id>/...`.
- **Dependencies**: none new. `flask`, `psycopg`, and `python-dotenv` are already in `requirements.txt`.
- **Data**: writes go to `follows` and `user_rankings`. The seed script stays re-runnable, so you can reset after manual testing.
- **Docs**: the code comments reference `specs/backend_api_feature.md`, which doesn't exist in the repo. This change's specs become the source of truth for the endpoint inventory.
