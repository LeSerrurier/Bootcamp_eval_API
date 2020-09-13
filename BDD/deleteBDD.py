import sqlite3

def supprimerBDD() :
    conn = sqlite3.connect("BDD/paulEmploi.db")
    
    conn.execute("DROP TABLE IF EXISTS adresse")
    conn.execute("DROP TABLE IF EXISTS personne")
    conn.execute("DROP TABLE IF EXISTS entreprise")
    conn.execute("DROP TABLE IF EXISTS embaucher")
    
    conn.commit()