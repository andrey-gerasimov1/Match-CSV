import sqlite3

conn = sqlite3.connect("matchme.db")
c = conn.cursor()

for row in c.execute("SELECT * FROM matched"):
    print(row)

conn.close()
