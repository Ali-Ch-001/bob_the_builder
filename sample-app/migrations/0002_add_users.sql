-- 0002_add_users.sql
-- depends_on: 0003

CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL
);
