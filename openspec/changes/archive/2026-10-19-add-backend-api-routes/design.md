# Design

## Context

- The backend uses Flask with one Blueprint per feature (`app/routes/*.py`), all registered in `app/main.py`. `routes/users.py` is the model to follow: each handler opens a connection with `with get_connection() as conn:`, runs parameterized SQL, and returns dicts or lists, which Flask serializes to JSON. Errors are returned as `{"error": ...}, <status>`.
- `get_connection()` uses psycopg 3 with `dict_row`. In psycopg 3, `with psycopg.connect(...) as conn:` commits when the block exits normally and rolls back if an exception is raised. So everything inside one `with` block is a single transaction.
- `schema.sql` uses `id INT PRIMARY KEY`, not `SERIAL` as described in CLAUDE.md. Inserts must supply an id. `create_user` already does this with `(SELECT COALESCE(MAX(id), 0) + 1 FROM users)`.
- `routes/feed.py` currently has no `bp` (uncommitted edit), so the app fails on import.
- `app/db.py` hardcodes `.../Beli`, while `.env.example` uses `.../beli`. `python-dotenv` is installed but never loaded.
- The endpoint numbers in the TODO comments (#1–#11) point to `specs/backend_api_feature.md`, which isn't in the repo. The delta specs in this change replace it.

## Goals / Non-Goals

**Goals:**
- Implement every endpoint in the specs, using the same style as `users.py`.
- Run each multi-row ranking change as one transaction, and validate in app code everything the schema doesn't enforce.

**Non-Goals:**
- Schema changes (switching to `SERIAL`, adding `UNIQUE`/`NOT NULL`). The schema's light constraints are intentional.
- Reordering existing ranking entries, pagination cursors, CORS, auth, or an automated test framework.

## Decisions

### Endpoint layout

| # | Method & path | File |
|---|---|---|
| 1 | `GET /users` | users.py (exists) |
| 2 | `GET /users/<id>` | users.py (exists) |
| 3 | `GET /restaurants?q=&cuisine=&city=` | restaurants.py |
| – | `GET /restaurants/<id>` | restaurants.py |
| 4 | `GET /users/<id>/rankings` | rankings.py |
| 5 | `GET /users/<id>/following` | follows.py |
| 6 | `GET /users/<id>/followers` | follows.py |
| 7 | `GET /users/<id>/feed?limit=` | feed.py |
| 8 | `POST /users/<id>/following` body `{followee_id}` | follows.py |
| 9 | `DELETE /users/<id>/following/<followee_id>` | follows.py |
| 10 | `POST /users/<id>/rankings` body `{restaurant_id, rank_position}` | rankings.py |
| 11 | `DELETE /users/<id>/rankings/<restaurant_id>` | rankings.py |

Each user-scoped route is nested under `/users/<id>`, because there's no auth and the frontend passes the current user's id. Follow and unfollow use the `following` collection so that POST and DELETE work on the same resource that GET lists. *Alternative:* a flat `/follows` resource with both ids in the body. That's harder to read and doesn't match the GET routes.

### Ranking commit takes a 1-based `rank_position`
The frontend runs the binary-search loop and sends `lo + 1`. The backend rejects values outside `1..n+1`. *Alternative:* send a 0-based index. Rejected because the stored column is 1-based, and translating between the two is a source of off-by-one bugs.

### Transactions and id assignment
`POST /rankings` uses one `with get_connection()` block that runs these steps in order:
1. Check that the user and restaurant exist.
2. Check that the restaurant isn't already on the list.
3. Read `n` and validate the position.
4. Shift rows down: `UPDATE user_rankings SET rank_position = rank_position + 1 WHERE user_id = %s AND rank_position >= %s`.
5. Insert the new row with `id = COALESCE(MAX(id),0)+1` and `created_at = now()`.

`DELETE` works the same way: delete the row (`RETURNING rank_position`), then shift the rows below it up by one. If any step returns an error, the code returns before the block finishes. Because no writes have happened at that point, nothing is committed. Since there's no unique constraint on `(user_id, rank_position)`, the shift can't hit a temporary collision. *Alternative:* `SELECT ... FOR UPDATE` row locking. That's not needed for a single local user, and it's noted under Risks.

### Search uses `ILIKE` on `lower(name)`
The query is `WHERE lower(name) LIKE lower(%s)` with `'%' + q + '%'` passed as a parameter, and `lower(cuisine) = lower(%s)` / `lower(city) = lower(%s)` added only when those filters are given. The filter clauses are built from fixed SQL fragments, and the values are always passed as parameters, never formatted into the SQL. Wildcard characters (`%`, `_`) in `q` are passed through as-is, which is acceptable for learning.

### Shared helpers stay minimal
A small `user_exists(conn, user_id)` check is repeated in several routes. Put it in `app/db.py` so every route returns the same 404 behavior. Don't add any other abstraction layer.

### Score computed in SQL
`ROUND(10.0 * (COUNT(*) OVER () - rank_position + 1) / COUNT(*) OVER (), 1)` computes the score in the list query, so it's never stored. *Alternative:* compute it in Python. That works equally well, but doing it in SQL keeps the score next to the data it depends on.

### Load DATABASE_URL from `.env`
`app/db.py` calls `load_dotenv()` and reads `os.environ["DATABASE_URL"]`, as CLAUDE.md requires. Check that the user's `.env` has the correct database name (`beli` vs `Beli`).

## Risks / Trade-offs

- [Two concurrent inserts could compute the same `MAX(id)+1` or interleave shifts] → Acceptable for a single-user local app. To harden it later, switch to `SERIAL` or lock the user's rows.
- [Manual testing writes to the seeded DB] → Re-run `schema.sql` + `seed.sql` to reset.
- [No automated tests] → Each task is verified with `curl` against the freshly seeded data. The scenarios in the specs work as the checklist.
