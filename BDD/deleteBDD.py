import sqlite3

conn = sqlite3.connect("paulEmploi.db")

conn.execute("DROP TABLE IF EXISTS adresse")
conn.execute("DROP TABLE IF EXISTS personne")
conn.execute("DROP TABLE IF EXISTS entreprise")
conn.execute("DROP TABLE IF EXISTS embaucher")