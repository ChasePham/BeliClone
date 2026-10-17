
DROP TABLE IF EXISTS user_rankings;
DROP TABLE IF EXISTS follows;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id           SERIAL PRIMARY KEY,
    username     TEXT,
    display_name TEXT,
    created_at   TIMESTAMPTZ
);

CREATE TABLE follows (
    follower_id INT,
    followee_id INT,
    created_at  TIMESTAMPTZ,

    PRIMARY KEY (follower_id, followee_id),
    CHECK (follower_id <> followee_id)
);

CREATE TABLE restaurants (
    id      SERIAL PRIMARY KEY,
    name    TEXT NOT NULL,
    cuisine TEXT,
    city    TEXT,
    address TEXT
);

-- Expression index so searches on lower(name) can use it.
CREATE INDEX restaurants_lower_name_idx ON restaurants (lower(name));

CREATE TABLE user_rankings (
    id            SERIAL PRIMARY KEY,
    user_id       INT,
    restaurant_id INT,
    rank_position INT,
    created_at    TIMESTAMPTZ

);
