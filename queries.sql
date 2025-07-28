-- Query 1: Count of customers that ordered yesterday and have at least another order in the past
SELECT COUNT(DISTINCT o1.customer_id)
FROM orders o1
JOIN orders o2 ON o1.customer_id = o2.customer_id
WHERE DATE(o1.order_date) = CURDATE() - INTERVAL 1 DAY
  AND o2.order_date < o1.order_date;

-- Query 2: List of customers who has more than 1 order ( at all the time ), extract customer name and the order id of the second order.
WITH ranked_orders AS (
  SELECT customer_id, order_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_rank
  FROM orders
)
SELECT c.customer_name, r.order_id AS second_order_id
FROM ranked_orders r
JOIN customers c ON r.customer_id = c.customer_id
WHERE r.order_rank = 2;