import sqlite3


bdd = sqlite3.connect('BDD/paulEmploi.db', check_same_thread=False)
bdd.row_factory = sqlite3.Row
response = bdd.execute("SELECT * FROM entreprise").fetchall()

for row in response :
    print(row[0])
    print(row[1])
    print(row[2])