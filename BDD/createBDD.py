import sqlite3

def creerBDD():
    conn = sqlite3.connect('BDD/paulEmploi.db')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS adresse (
                 id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                 ville TEXT,
                 codePostal INTEGER,
                 rue TEXT,
                 numeroRue INTEGER )''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS personne
                (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                 prenom TEXT NOT NULL,
                 rechercheEntreprise NUMERIC NOT NULL,
                 idAdresse INTEGER,
                 motDePasse TEXT NOT NULL,
                 FOREIGN KEY(idAdresse) REFERENCES adresse(id));''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS entreprise
                 (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                  nom  TEXT NOT NULL,
                  rechercheSalarie NUMERIC NOT NULL,
                  idAdresse INTEGER NOT NULL,
                  motDePasse TEXT NOT NULL,
                  FOREIGN KEY(idAdresse) REFERENCES adresse(id));''')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS embaucher
                 (idPersonne INTEGER NOT NULL,
                 idEntreprise INTEGER NOT NULL,
                 nombreJourContrat INTEGER NOT NULL,
                 PRIMARY KEY(idPersonne, idEntreprise),
                 FOREIGN KEY(idPersonne) REFERENCES personne(id),
                 FOREIGN KEY(idEntreprise) REFERENCES entreprise(id));''')
    
    
    conn.execute("INSERT INTO adresse (ville, codePostal, rue, numeroRue) VALUES ('Toulouse', 31200, 'Des caprices', 5)");
    conn.execute("INSERT INTO adresse (ville, codePostal, rue, numeroRue) VALUES ('Tournefeuille', 31170, 'Des chats', 45)");
    conn.execute("INSERT INTO adresse (ville, codePostal, rue, numeroRue) VALUES ('Labege', 31670, 'Des objets', 50)");
    conn.execute("INSERT INTO adresse (ville, codePostal, rue, numeroRue) VALUES ('Toulouse', 31200, 'La residence', 31)");
    
    
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Paul', 1, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Gerard', 1, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Lea', 1, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Anthony', 0, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Toto', 0, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Tata', 0, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Titi', 0, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Tutu', 0, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Mumu', 0, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('Mimi', 0, 4, 'motdepasse')");
    conn.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('root', 0, null, 'root')");
    
    
    conn.execute("INSERT INTO entreprise (nom, rechercheSalarie, idAdresse, motDePasse) VALUES ('Airbus', 1, 1, 'motdepasse')");
    conn.execute("INSERT INTO entreprise (nom, rechercheSalarie, idAdresse, motDePasse) VALUES ('CapGemini', 1, 2, 'motdepasse')");
    conn.execute("INSERT INTO entreprise (nom, rechercheSalarie, idAdresse, motDePasse) VALUES ('Sogeti', 0, 3, 'motdepasse')");
    
    conn.execute("INSERT INTO embaucher (idPersonne, idEntreprise, nombreJourContrat) VALUES (4,1, 30)");
    conn.execute("INSERT INTO embaucher (idPersonne, idEntreprise, nombreJourContrat) VALUES (5,1, 60)");
    conn.execute("INSERT INTO embaucher (idPersonne, idEntreprise, nombreJourContrat) VALUES (6,2, 15)");
    conn.execute("INSERT INTO embaucher (idPersonne, idEntreprise, nombreJourContrat) VALUES (7,3, 125)");
    conn.execute("INSERT INTO embaucher (idPersonne, idEntreprise, nombreJourContrat) VALUES (8,3, 90)");
    
    conn.commit() 
    
    conn.close()