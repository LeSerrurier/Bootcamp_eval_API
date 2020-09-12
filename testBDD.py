import sqlite3


bdd = sqlite3.connect('BDD/paulEmploi.db', check_same_thread=False)
bdd.row_factory = sqlite3.Row
response = bdd.execute("SELECT * FROM personne WHERE prenom LIKE 'dd'").fetchone()
print(response)
if not response :
    print("none")
else :
    print("oui")