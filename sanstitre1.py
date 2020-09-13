import sqlite3

bdd = sqlite3.connect('BDD/paulEmploi.db')

res = bdd.execute("""SELECT * FROM entreprise as ent, personne as per, embaucher as emb
                     WHERE ent.id = emb.idEntreprise
                     AND per.id = emb.idPersonne
                     AND ent.nom LIKE 'Airbus'""").fetchone()
print(res[0])