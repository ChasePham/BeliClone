
DROP TABLE IF EXISTS user_rankings;
DROP TABLE IF EXISTS follows;
DROP TABLE IF EXISTS restaurants;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id           INT PRIMARY KEY,
    username     TEXT,
    display_name TEXT,
    created_at   TIMESTAMPTZ
);

CREATE TABLE follows (
    follower_id INT REFERENCES users (id),
    followee_id INT REFERENCES users (id),
    created_at  TIMESTAMPTZ,

    PRIMARY KEY (follower_id, followee_id),
    CHECK (follower_id <> followee_id)
);

CREATE TABLE restaurants (
    id      INT PRIMARY KEY,
    name    TEXT NOT NULL,
    cuisine TEXT,
    city    TEXT,
    address TEXT
);

-- Expression index so searches on lower(name) can use it.
CREATE INDEX restaurants_lower_name_idx ON restaurants (lower(name));

CREATE TABLE user_rankings (
    id            INT PRIMARY KEY,
    user_id       INT REFERENCES users (id),
    restaurant_id INT REFERENCES restaurants (id),
    rank_position INT,
    created_at    TIMESTAMPTZ

);
