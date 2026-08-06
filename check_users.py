from database import get_connection

conn = get_connection()
cur = conn.cursor()
cur.execute("SELECT current_database();")
print("Connected to:", cur.fetchone())

cur.execute("SELECT id, username, email, created_at FROM users;")
rows = cur.fetchall()
print("Row count:", len(rows))
for row in rows:
    print(row)

cur.close()
conn.close()