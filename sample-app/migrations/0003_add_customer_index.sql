-- 0003_add_customer_index.sql
-- depends_on: 0001

CREATE INDEX idx_orders_customer ON orders (customer);
