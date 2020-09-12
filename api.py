import uuid
import sqlite3
from flask import Flask, jsonify, request, session, abort
from functools import wraps

app = Flask(__name__)

bdd = sqlite3.connect('BDD/paulEmploi.db', check_same_thread=False)
bdd.row_factory = sqlite3.Row

def verif_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = request.form
        token = data["token"]
        if "token" not in data or token not in session:
            return jsonify({"token": False})
        session[token].update({"token": True})
        return f(*args, **kwargs)
    return decorator


@app.route("/connexion", methods=['GET'])
def connexion():
    jsonSiErreur = "Les informations ne sont pas conformes"
    data = request.args
    if "identite" in data and "typeCompte" in data and "motdepasse" in data :
        typeCompte = data["typeCompte"]
        identite = data["identite"]
        motdepasse = data["motdepasse"]
        
        if typeCompte != "personne" and typeCompte != "entreprise" :
            return jsonify({"connexion": jsonSiErreur})

        if typeCompte == "entreprise" :
            existe = bdd.execute("SELECT * FROM entreprise WHERE nom LIKE'" + identite + "'").fetchone()
        if typeCompte == "personne" :
            existe = bdd.execute("SELECT * FROM personne WHERE prenom LIKE '" + identite + "'").fetchone()
        if not existe or existe["motdepasse"] != motdepasse : 
            return jsonify({"connexion": jsonSiErreur})
        
        token = str(uuid.uuid4())
        session[token] = {"typeCompte": data["typeCompte"],
                          "identite": data["identite"]}
        return jsonify({"connexion": "reussi", "token": token})
    
    return jsonify({"connexion": jsonSiErreur})

@app.route("/profil/<identite>", methods=["POST"])
@verif_token
def profil(identite):
    infoPersonne = bdd.execute("SELECT * FROM personne WHERE prenom LIKE '" + identite + "'")
    information = {}
    for row in infoPersonne:
        information.update({"prenom" : row[1], "recherche entreprise" : row[2]})
    return jsonify(information)

       

if __name__ == '__main__':
    app.secret_key = 'pass'
    app.run()