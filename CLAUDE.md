# BeliClone

A local-only clone of the Beli restaurant-ranking app, built for learning. It covers the core features only: users, follows, ranked "been" lists, a feed, and restaurant search.

## Project constraints

- **Local only.** Nothing is deployed or published to the cloud. No cloud services, hosted databases, or third-party APIs (no Google Places, Yelp, etc.).
- **No real user data.** All users, restaurants, and follow relationships are hardcoded seed data.
- **Learning first.** Choose clear, readable implementations over clever or heavily optimized ones. Don't add production concerns (auth providers, caching layers, queues, containers) unless asked.
- **Core features only.** Don't build reviews, photos, maps, notifications, or lists beyond "been" unless asked.

## Tech stack

| Layer    | Technology            |
|----------|-----------------------|
| Database | PostgreSQL (local)    |
| Backend  | Python (REST API)     |
| Frontend | React                 |

The frontend calls the backend over HTTP; the backend is the only layer that talks to Postgres.

## Functional requirements

1. **Users**: The app has users (seeded). Picking the "current user" can be a simple switcher; real authentication is out of scope unless asked.
2. **Follows**: A user can follow and unfollow other users. Follows are one-directional (A following B doesn't mean B follows A).
3. **"Been" list with ranking**: A user adds a restaurant to their been list, and the app places it in their ranked list by asking a series of binary questions ("Which did you prefer: X or Y?"). See [Ranking algorithm](#ranking-algorithm).
4. **Feed**: A user sees recent ranking activity from the users they follow, newest first.
5. **Search**: A user can search restaurants by name (and optionally by cuisine or city).

## Database schema

Four tables, defined in `backend/db/schema.sql`. Column names here are the intended design; keep migrations and seed data consistent with them.

The schema deliberately keeps constraints light: there are no foreign keys, `NOT NULL`s, `UNIQUE`s, or `created_at` defaults beyond what's listed below. **Application code is responsible for data validity**, including:
- setting `created_at` on every insert (use `now()` in the SQL),
- only inserting ids that exist in the referenced table,
- keeping each user's `rank_position` values unique and contiguous,
- not adding the same restaurant to a user's list twice.

### `users`
| Column       | Type        | Notes                             |
|--------------|-------------|-----------------------------------|
| `id`         | SERIAL PK   |                                   |
| `username`   | TEXT        | should be unique (enforced by app)|
| `display_name` | TEXT      |                                   |
| `created_at` | TIMESTAMPTZ | set by app on insert              |

### `follows`
| Column        | Type        | Notes                         |
|---------------|-------------|-------------------------------|
| `follower_id` | INT (→ users.id) | the user doing the following |
| `followee_id` | INT (→ users.id) | the user being followed      |
| `created_at`  | TIMESTAMPTZ | set by app on insert          |

- PK `(follower_id, followee_id)`
- CHECK `follower_id <> followee_id` (a user can't follow themselves)

### `restaurants`
| Column     | Type      | Notes            |
|------------|-----------|------------------|
| `id`       | SERIAL PK |                  |
| `name`     | TEXT      | NOT NULL         |
| `cuisine`  | TEXT      |                  |
| `city`     | TEXT      |                  |
| `address`  | TEXT      |                  |

- Index on `lower(name)` for search.

### `user_rankings`
| Column          | Type        | Notes                                  |
|-----------------|-------------|----------------------------------------|
| `id`            | SERIAL PK   |                                        |
| `user_id`       | INT (→ users.id) |                                   |
| `restaurant_id` | INT (→ restaurants.id) |                             |
| `rank_position` | INT         | 1 = favorite; contiguous per user (enforced by app) |
| `created_at`    | TIMESTAMPTZ | when it was added; drives the feed; set by app on insert |

The feed has no separate posts table: it comes from `user_rankings` joined with `follows`, ordered by `created_at DESC`.

## Ranking algorithm

Adding a restaurant is a **binary insertion** driven by the user's answers:

1. Load the user's current list ordered by `rank_position` (size `n`).
2. If `n == 0`, insert at position 1.
3. Otherwise binary search: keep `lo = 0`, `hi = n`. Compare the new restaurant against the one at index `mid = (lo + hi) // 2`.
   - User prefers the new one → `hi = mid`
   - User prefers the existing one → `lo = mid + 1`
4. When `lo == hi`, the new restaurant goes in at index `lo` (position `lo + 1`).
5. In **one transaction**: shift every row with `rank_position >= lo + 1` down by one, then insert the new row.

This takes about `log2(n)` comparisons. The comparison loop can live on the frontend (it holds `lo`/`hi` and asks the user) with a single final `POST` to commit the position, or on the backend as a stateful session. Prefer the frontend loop plus one commit endpoint, since it's simpler. The backend must still check that the final position is in range and do the shift and insert atomically.

Removing a restaurant shifts everything below it up by one, also in one transaction.

An optional score shown to users (like Beli's 0–10) can be calculated from position, e.g. `10 * (n - position + 1) / n`. Don't store it.

## Seed data

Hardcoded seed data lives in a SQL or Python seed script and must be re-runnable (drop/recreate or truncate before inserting). It should include:
- ~5–10 users
- ~20–50 restaurants across a few cuisines and cities
- A follow graph with some mutual and some one-way follows
- A few pre-ranked been lists so the feed and rankings have data

## Repository layout

```
BeliClone/
├── CLAUDE.md
├── specs/        # feature specs and design notes
├── backend/      # Python API, DB access, migrations, seed script
└── frontend/     # React app
```

`specs/` holds the feature specs. Check it before building a feature.

## Commands

_To be filled in once the backend and frontend are scaffolded (setup, run, seed, test)._

## Conventions

- Use parameterized SQL queries only. Never build SQL with string formatting.
- Any multi-row ranking change (insert, delete, reorder) happens in a single transaction.
- Keep database access in the backend; the React app never connects to Postgres directly.
- Secrets/config (DB URL) come from a local `.env` file, which is git-ignored.
