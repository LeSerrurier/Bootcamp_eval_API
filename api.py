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
    data = request.form
    token = data["token"]

    if identite != session[token]["identite"] :
        return jsonify({"erreur": "Ce n'est pas votre compte"})

    if session[token]["typeCompte"] == "personne" :
        infoEntite = bdd.execute("SELECT * FROM personne, adresse WHERE personne.idAdresse = adresse.id AND prenom LIKE '" + identite + "'").fetchone()
        jsonReturn = {"prenom" : infoEntite["prenom"], "recherche entreprise" : infoEntite["rechercheEntreprise"]}
    elif session[token]["typeCompte"] == "entreprise" :
        infoEntite = bdd.execute("SELECT * FROM entreprise, adresse WHERE entreprise.idAdresse = adresse.id AND nom LIKE '" + identite + "'").fetchone()
        jsonReturn = {"nom" : infoEntite["nom"], "recherche salarie" : infoEntite["rechercheSalarie"]}
    else :
        return jsonify({"erreur": "Type de compte non reconnu"})
    
    jsonReturn.update({"ville": infoEntite["ville"], "code postal": infoEntite["codePostal"], "rue": infoEntite["rue"], "numero rue": infoEntite["numeroRue"]})
    return jsonify(jsonReturn)
    
@app.route("/admin/personne/delete/<prenom>", methods=["DELETE"])
@verif_token
def supprimerPersonne(prenom) :
    data = request.form
    token = data["token"]
    
    if "root" != session[token]["identite"] :
        return jsonify({"erreur": "Vous n'avez pas les droits"})
    
    verifExistant = bdd.execute("SELECT * FROM personne WHERE prenom LIKE '%" + prenom + "'").fetchone()
    if not verifExistant :
        return jsonify({"erreur": "Personne inexistante"})
    
    #bdd.execute("DELETE FROM TABLE personne WHERE prenom LIKE '%'" + prenom + "'")
    #bdd.execute("commit")
    
    return jsonify({"suppression": True, "prenom": prenom})

if __name__ == '__main__':
    app.secret_key = 'pass'
    app.run()