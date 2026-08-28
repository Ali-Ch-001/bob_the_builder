-- 0001_create_orders.sql
-- depends_on: (none)

CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    customer TEXT NOT NULL,
    items TEXT NOT NULL,
    total REAL NOT NULL
);
