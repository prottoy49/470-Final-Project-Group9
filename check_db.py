import sqlite3

# Connect to the database
conn = sqlite3.connect('closet_items.db')
cursor = conn.cursor()

# Fetch all rows from closet_items table
cursor.execute("SELECT * FROM closet_items")
rows = cursor.fetchall()

# Display the results
for row in rows:
    print(row)

# Close the connection
conn.close()
