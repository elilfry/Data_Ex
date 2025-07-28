import mysql.connector
from datetime import datetime, timedelta
import random
import string

# Database connection
db = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="enter-your-password",  # important - enter your password
    database="ecommerce"
)
cursor = db.cursor()

# Function to generate a random name
def random_name():
    return ''.join(random.choices(string.ascii_uppercase, k=5))

# Function to generate a random email based on name
def random_email(name):
    return f"{name.lower()}@example.com"

# Generate 1,000 customers
end_date = datetime(2025, 7, 28)  # Today
start_date = end_date - timedelta(days=90)  # 3 months back
customer_ids = []  # To store generated customer IDs
for _ in range(1000):
    name = random_name()
    email = random_email(name)
    signup_date = start_date + timedelta(days=random.randint(0, 90))
    sql = "INSERT INTO customers (customer_name, email, signup_date) VALUES (%s, %s, %s)"
    cursor.execute(sql, (name, email, signup_date))
    customer_ids.append(cursor.lastrowid)

# Generate products (if not already done)
products = []
for i in range(1, 6):  # 5 products
    sql = "INSERT INTO products (product_name, current_price) VALUES (%s, %s)"
    cursor.execute(sql, (f"Product_{i}", round(random.uniform(5, 100), 2)))
    products.append(cursor.lastrowid)

# Generate 10,000 orders per month for 3 months
for month in range(3):
    month_start = datetime(2025, 4 + month, 1)
    for _ in range(10000):
        customer_id = random.choice(customer_ids)
        order_date = month_start + timedelta(days=random.randint(0, 30))
        total_amount = round(random.uniform(10, 500), 2)
        sql = "INSERT INTO orders (customer_id, order_date, total_amount) VALUES (%s, %s, %s)"
        cursor.execute(sql, (customer_id, order_date, total_amount))
        
        order_id = cursor.lastrowid
        product_id = random.choice(products)
        quantity = random.randint(1, 5)
        price = round(random.uniform(5, 100), 2)
        sql = "INSERT INTO order_items (order_id, product_id, current_price, quantity) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (order_id, product_id, price, quantity))

# Generate some cart entries
for _ in range(500):
    customer_id = random.choice(customer_ids)
    product_id = random.choice(products)
    quantity = random.randint(1, 3)
    added_date = datetime.now() - timedelta(days=random.randint(0, 30))
    sql = "INSERT INTO cart (customer_id, product_id, quantity, added_date) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (customer_id, product_id, quantity, added_date))

# Generate logins for each customer (1-5 logins per customer)
for customer_id in customer_ids:
    num_logins = random.randint(1, 5)  # Random number of logins per customer
    for _ in range(num_logins):
        login_date = start_date + timedelta(days=random.randint(0, 90))  # Within 3 months
        # Optionally link to a visit_id (since visits is empty, set to NULL)
        sql = "INSERT INTO logins (customer_id, login_date, visit_id) VALUES (%s, %s, %s)"
        cursor.execute(sql, (customer_id, login_date, None))

# Commit changes and close connection
db.commit()
db.close()

print("Data generation completed successfully!")