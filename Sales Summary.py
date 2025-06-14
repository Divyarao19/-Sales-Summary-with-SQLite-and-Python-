# SALES SUMMARY

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("sales_data.db")
cursor = conn.cursor()

# Create the sales table
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    quantity INTEGER NOT NULL,
    price REAL NOT NULL
)
""")

# Insert sample sales data
cursor.execute("SELECT COUNT(*) FROM sales")
if cursor.fetchone()[0] == 0:
    sample_data = [
        ("Apples", 10, 0.50),
        ("Bananas", 5, 0.30),
        ("Oranges", 8, 0.60),
        ("Apples", 7, 0.50),
        ("Bananas", 10, 0.30)
    ]
    cursor.executemany("INSERT INTO sales (product, quantity, price) VALUES (?, ?, ?)", sample_data)
    conn.commit()

# Run SQL query to summarize sales
query = """
SELECT
    product,
    SUM(quantity) AS total_qty,
    SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""
df = pd.read_sql_query(query, conn)

# Print the results
print("Sales Summary:")
print(df)

# Plot a simple bar chart of revenue by product
plt.figure(figsize=(8, 5))
df.plot(kind='bar', x='product', y='revenue', color='orange', legend=False)
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.show()

conn.close()
