# Tasks

Verification throughout: re-seed with `psql -d Beli -f backend/db/schema.sql -f backend/db/seed.sql`, run `cd backend && python -m app.main` (port 5001), then hit the endpoints with `curl`.

## 1. Backend foundation

- [x] 1.1 Restore `bp = Blueprint('feed', __name__)` in `app/routes/feed.py` and verify `python -m app.main` starts and `curl localhost:5001/` returns `{"status": "ok"}`
- [x] 1.2 Make `app/db.py` load `DATABASE_URL` from `backend/.env` via `python-dotenv` (remove the hardcoded URL) and verify `curl localhost:5001/users` still returns the 8 seeded users
- [x] 1.3 Add a `user_exists(conn, user_id)` helper in `app/db.py` and verify it by using it in the first route that needs it (task 3.1)

## 2. Restaurant search

- [x] 2.1 Implement `GET /restaurants` with `q`, `cuisine`, and `city` params (parameterized, case-insensitive) and verify that `?q=golden` returns 3 results, `?q=golden&city=chicago` returns 1, and `?q=zzzz` returns `[]`
- [x] 2.2 Implement `GET /restaurants/<id>` and verify `/restaurants/2` returns Sora Ramen and `/restaurants/9999` returns 404

## 3. "Been" rankings

- [x] 3.1 Implement `GET /users/<id>/rankings` (joined with restaurants, ordered by position, with computed `score`) and verify user 2 returns positions 1–4 with scores 10.0/7.5/5.0/2.5, and user 9999 returns 404
- [x] 3.2 Implement `POST /users/<id>/rankings` (validate the user, restaurant, and duplicate entry; validate `rank_position` is in `1..n+1`; then shift and insert in one transaction) and verify that inserting restaurant 3 at position 2 for user 1 yields contiguous positions 1–4 with it at 2
- [x] 3.3 Verify the add error paths with curl: position 0 and n+2 return 400, a duplicate restaurant returns 409, an unknown restaurant returns 404, and the list is unchanged after each
- [x] 3.4 Implement `DELETE /users/<id>/rankings/<restaurant_id>` (delete and shift up in one transaction, 204/404) and verify that removing the middle entry leaves positions 1..n-1 with no gaps

## 4. Follows

- [x] 4.1 Implement `GET /users/<id>/following` and `GET /users/<id>/followers` and verify user 1 follows {2,3,4,7}, has followers {2,3,5,6}, and unknown users return 404
- [x] 4.2 Implement `POST /users/<id>/following` with `{followee_id}` (400 for self or bad input, 404 for an unknown user, 409 for a duplicate) and verify a 4→1 follow appears in user 4's following but not in user 1's following
- [x] 4.3 Implement `DELETE /users/<id>/following/<followee_id>` (204/404) and verify that after `DELETE /users/1/following/7`, user 7 is gone from user 1's following

## 5. Feed

- [x] 5.1 Implement `GET /users/<id>/feed` (join follows to user_rankings, users, and restaurants, order by `created_at DESC`, `limit` default 50 within 1–100) and verify that a freshly seeded user 1's feed only contains users 2/3/4/7, is newest-first, and that `?limit=3` returns 3 items and `?limit=abc` returns 400

## 6. Integration check

- [x] 6.1 Re-seed, then walk through the end-to-end flow with curl: user 1 follows user 5, user 5 adds a restaurant via POST, it appears at the top of user 1's feed, user 5 removes it, and it disappears from the feed. Verify each step's status code and body match the specs
- [x] 6.2 Replace the stale `specs/backend_api_feature.md` references in route comments with a pointer to this change's specs, and fill in the Commands section of `CLAUDE.md` (run and seed). Verify the documented commands work as written
