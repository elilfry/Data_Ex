
## Step 1: Environment Setup

###  Install Required Tools

- **MySQL**
- **Python 3.10+**
  

##  Step 2: Create the Database Schema
- CMD
```bash
mysql -u root -p
DROP DATABASE IF EXISTS ecommerce;
CREATE DATABASE ecommerce;
```

- Exit the MySQL shell and run:
```bash
mysql -u root -p ecommerce < schema1.sql

```

##  Step 3: Create Conda Environment

```bash
conda create -n ecommerce-env python=3.10 -y
conda activate ecommerce-env
```

## Step 4: Install Dependencies
```bash
pip install -r requirements.txt

```

## Step 5: Generate Synthetic Data

- Important:
Before running the script, open data_gen.py and update the MySQL connection details:

```python
db = mysql.connector.connect(
    user='root',
    password='your_password_here',  # <--- INSERT YOUR PASSWORD
    host='localhost',
    database='ecommerce'
)
```

```python
python data_gen.py
```
- You should see:
" Data generation completed successfully!"

## Step 6: Run Analytics Queries

Q1: Customers who ordered yesterday and had past orders
```bash

SELECT COUNT(DISTINCT o1.customer_id)
FROM orders o1
JOIN orders o2 ON o1.customer_id = o2.customer_id
WHERE DATE(o1.order_date) = CURDATE() - INTERVAL 1 DAY
  AND o2.order_date < o1.order_date;
```

 Q2: Second order ID per customer
```bash

WITH ranked_orders AS (
  SELECT customer_id, order_id,
         ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) AS order_rank
  FROM orders
)
SELECT c.customer_name, r.order_id AS second_order_id
FROM ranked_orders r
JOIN customers c ON r.customer_id = c.customer_id
WHERE r.order_rank = 2;
```

