
import csv
import sqlite3
from difflib import SequenceMatcher

conn = sqlite3.connect("matchme.db")
c = conn.cursor()
c.execute("DROP TABLE IF EXISTS matched")
c.execute("""
    CREATE TABLE matched (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name1 TEXT,
        name2 TEXT,
        score REAL
    )
""")

def load_csv(path):
    with open(path, newline='', encoding='utf-8') as csvfile:
        return list(csv.DictReader(csvfile))

def match_score(a, b):
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

csv1 = [
    {"name": "Coalition Inc"},
    {"name": "Blue Shield"},
    {"name": "Allied Brokers"}
]

csv2 = [
    {"name": "Coalition Incorporated"},
    {"name": "BlueShield Health"},
    {"name": "Ally Brokers Group"}
]

for row1 in csv1:
    best_match = None
    best_score = 0
    for row2 in csv2:
        score = match_score(row1["name"], row2["name"])
        if score > best_score:
            best_match = row2["name"]
            best_score = score
    c.execute("INSERT INTO matched (name1, name2, score) VALUES (?, ?, ?)",
              (row1["name"], best_match, best_score))

conn.commit()
conn.close()
