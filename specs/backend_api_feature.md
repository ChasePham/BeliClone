# Backend API: Feature Spec

| Field        | Value |
|--------------|-------|
| Status       | Draft |
| Framework    | Flask |

---

## 1. Goal

Expose the five core features from CLAUDE.md (users, follows, rankings, feed, search) as HTTP endpoints that return JSON. The backend is the only layer that talks to Postgres.

What "done" means for this spec:
- [ ] Every endpoint in [Endpoint inventory](#8-endpoint-inventory) is implemented and manually tested
- [ ] The React app can call every endpoint it needs

---

## 2. Constraints (from CLAUDE.md)

- Local only: no cloud services or third-party APIs.
- Parameterized SQL only. Never build SQL with f-strings or `+`.
- Any multi-row ranking change (insert, delete, reorder) happens in **one transaction**.
- `DATABASE_URL` comes from `backend/.env` (git-ignored).
- No auth. The "current user" is passed explicitly (decide how in [Conventions](#7-conventions)).
- The schema keeps constraints light, so **the API enforces data validity** (see [App-enforced rules](#11-app-enforced-rules-checklist)).

---

## 3. Setup checklist

### Shared (do these once)
- [ ] Add a `.gitignore` at the repo root covering: `.env`, `venv/`, `__pycache__/`, `node_modules/`
- [ ] Create a virtual environment in `backend/` and activate it
- [ ] Create `backend/.env` with `DATABASE_URL=postgresql://<mac-username>@localhost:5432/beliclone`
- [ ] Create `backend/.env.example` (same keys, placeholder values; this one *is* committed)
- [ ] Create `backend/requirements.txt`
- [ ] Database is created and seeded (`schema.sql` then `seed.sql`)

### Packages
| Purpose | Package |
|---------|---------|
| Web framework | `flask` |
| Postgres driver | `psycopg[binary]` (psycopg 3) |
| Read `.env` | `python-dotenv` |
| CORS for React (later) | `flask-cors` |
| Tests (later) | `pytest` |

### Run command
- Dev server: ___ (e.g. `flask --app <module> run --debug --port 5001`)
- **Port note:** Flask defaults to port 5000, which macOS's AirPlay Receiver usually already uses. Use 5001 (or turn off AirPlay Receiver in System Settings).

> Once this works, copy it into the **Commands** section of CLAUDE.md.

---

## 4. Folder layout

```
backend/
├── .env                 # git-ignored
├── .env.example
├── requirements.txt
├── db/
│   ├── schema.sql
│   └── seed.sql
└── app/
    ├── main.py          # creates the app object, registers route groups
    ├── db.py            # reads DATABASE_URL, opens connections
    └── routes/
        ├── users.py
        ├── follows.py
        ├── rankings.py
        ├── feed.py
        └── restaurants.py
```

| File | What goes there |
|------|-----------------|
| `main.py` | `Flask(__name__)`, `register_blueprint(...)` for each route file |
| `routes/*.py` | one `Blueprint` per feature |
| `db.py` | reads `DATABASE_URL`, opens connections |

---

## 5. Flask quick reference

Use this when translating an endpoint spec into code.

| I need to… | Flask |
|------------|-------|
| Define a route | `@bp.get("/path")` (also `.post`, `.delete`, …) |
| Read a path param (`/users/<id>`) | `<int:user_id>` in the path + matching function arg |
| Read a query param (`?q=`) | `request.args.get("q")` |
| Read a JSON body | `request.get_json()` |
| Return JSON | return a dict/list (or `jsonify`) |
| Set a status code | `return body, 201` |
| Return an error | `abort(404)` or `return {"error": ...}, 404` |
| Validate input | `if` checks in your function |

---

## 6. Database access pattern

Decide and write down how each request talks to Postgres:

- [ ] **Connection:** `db.py` reads `DATABASE_URL` once at startup (via `python-dotenv`)
- [ ] **Per request:** open a connection, use it, close it (simplest; a pool can come later if ever)
- [ ] **Rows as dicts:** use psycopg's `dict_row` row factory so rows convert to JSON easily
- [ ] **Placeholders:** psycopg uses `%s` (or `%(name)s`) and you pass values separately. Never format them into the string
- [ ] **Transactions:** wrap multi-statement writes in `with conn.transaction():` so they all commit or all roll back
- [ ] **Errors:** decide what happens when psycopg raises (e.g. foreign key violation → `404` or `400`?) ___

---

## 7. Conventions

| Topic | Decision |
|-------|----------|
| Base URL | ___ (e.g. `http://localhost:5001`) |
| URL prefix | ___ (none, or `/api`) |
| Current user | ___ (path segment `/users/<id>/...`, header `X-User-Id`, or query `?as=`) |
| Naming | ___ (plural nouns: `/users`, `/restaurants`; `snake_case` JSON keys to match columns) |
| Timestamps in JSON | ___ (ISO 8601 strings, e.g. `2026-10-17T16:25:30-04:00`) |
| Error body shape | ___ (e.g. `{"error": "message"}`; pick one shape and use it everywhere) |
| Pagination | ___ (e.g. `?limit=20`, default + max) |

### Status codes

| Code | Use it when |
|------|-------------|
| 200 OK | A successful read or update |
| 201 Created | A new row was created (follow, ranking) |
| 204 No Content | A successful delete with no body |
| 400 Bad Request | Input is malformed or breaks a rule (e.g. position out of range) |
| 404 Not Found | The user/restaurant/ranking in the URL doesn't exist |
| 409 Conflict | It already exists (e.g. already following, restaurant already ranked) |

---

## 8. Endpoint inventory

One row per endpoint. Fill in method + path, then write a full spec for each using [section 9](#9-endpoint-spec-template).

| # | Feature | Method | Path | Spec written | Done |
|---|---------|--------|------|:---:|:---:|
| 1 | Users: list | ___ | ___ | [ ] | [ ] |
| 2 | Users: get one | ___ | ___ | [ ] | [ ] |
| 3 | Search restaurants | ___ | ___ | [ ] | [ ] |
| 4 | Rankings: get a user's list | ___ | ___ | [ ] | [ ] |
| 5 | Follows: who a user follows | ___ | ___ | [ ] | [ ] |
| 6 | Follows: a user's followers | ___ | ___ | [ ] | [ ] |
| 7 | Feed | ___ | ___ | [ ] | [ ] |
| 8 | Follow | ___ | ___ | [ ] | [ ] |
| 9 | Unfollow | ___ | ___ | [ ] | [ ] |
| 10 | Rankings: add (commit final position) | ___ | ___ | [ ] | [ ] |
| 11 | Rankings: remove | ___ | ___ | [ ] | [ ] |
| 12 | ___ | ___ | ___ | [ ] | [ ] |

> Suggested build order is top to bottom: reads before writes, ranking writes last.

---

## 9. Endpoint spec template

Copy this block once per endpoint.

```markdown
### <#>. <Endpoint name>

**Purpose:** ___ (one sentence: what the user is trying to do)

**Method & path:** `___ ___`

**Path params**
| Name | Type | Notes |
|------|------|-------|
| ___  | ___  | ___   |

**Query params**
| Name | Type | Required? | Default | Notes |
|------|------|-----------|---------|-------|
| ___  | ___  | ___       | ___     | ___   |

**Request body** (JSON; writes only)
| Field | Type | Required? | Notes |
|-------|------|-----------|-------|
| ___   | ___  | ___       | ___   |

**Success response:** `___` (status code)
    (example JSON here)

**Error responses**
| Status | When |
|--------|------|
| ___    | ___  |

**Validation (app-enforced)**
- [ ] ___

**Database work**
- Tables touched: ___
- Query in plain English: ___
- Parameters passed: ___
- Needs a transaction? [ ] yes [ ] no. Why: ___

**Flask notes:** ___

**Manual test cases** (use seed data)
| Input | Expected |
|-------|----------|
| ___   | ___      |
```

---

## 10. Worked example (how to fill the template)

> Example only, showing the level of detail to aim for. No code.

### 1. List users

**Purpose:** Show every user so the frontend can offer a "current user" switcher.

**Method & path:** `GET /users`

**Path params:** none
**Query params:** none
**Request body:** none

**Success response:** `200`
```json
[
  { "id": 1, "username": "chasepham", "display_name": "Chase" },
  { "id": 2, "username": "helenkang", "display_name": "Helen" }
]
```

**Error responses:** none expected (an empty table returns `[]`)

**Validation:** none (no input)

**Database work**
- Tables touched: `users`
- Query in plain English: select id, username, display_name from users, ordered by id
- Parameters passed: none
- Needs a transaction? no: a single read

**Flask notes:** route on the `users` Blueprint; return the list of dict rows.

**Manual test cases**
| Input | Expected |
|-------|----------|
| `GET /users` after seeding | 8 users, ids 1–8 in order |

---

## 11. App-enforced rules checklist

The schema doesn't enforce these, so the API must. Note which endpoint handles each one.

| Rule | Enforced in endpoint # |
|------|------------------------|
| Every insert sets `created_at` (use `now()` in the SQL) | ___ |
| New rows get an `id` (your incrementer: e.g. `COALESCE(MAX(id), 0) + 1`) | ___ |
| `username` is unique | ___ |
| A restaurant appears at most once per user's list | ___ |
| `rank_position` stays unique and contiguous (1..n) per user | ___ |
| New position is in range `1..n+1` | ___ |
| Add = shift rows `>= position` down by 1, then insert, in one transaction | ___ |
| Remove = delete, then shift rows below up by 1, in one transaction | ___ |
| Can't follow yourself (the DB CHECK also catches this; return a clean `400`) | ___ |
| Referenced user/restaurant exists (the DB FK also catches this; return a clean `404`) | ___ |

---

## 12. Testing checklist

- [ ] Each endpoint tested by hand (`curl`, or a browser for GETs)
- [ ] Each error response triggered on purpose at least once
- [ ] After any ranking write: run the duplicate/contiguous checks from the seed step in `psql`
- [ ] Reseed (`schema.sql` + `seed.sql`) before a fresh round of testing
- [ ] (Later) `pytest` tests that reset the DB, call endpoints, and check responses

---

## 13. Open questions

- ___
- ___
