import uuid
import sqlite3
import helper
from flask import Flask, jsonify, request, session

app = Flask(__name__)

bdd = sqlite3.connect('BDD/paulEmploi.db', check_same_thread=False)
bdd.row_factory = sqlite3.Row

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
@helper.verif_token
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
    
@app.route("/admin/personne/voir/<prenom>", methods=["POST"])
@helper.verif_token
@helper.verif_root_personne
def voirPersone(prenom) :    
    reqPersonne = bdd.execute("SELECT * FROM personne, adresse WHERE personne.idAdresse = adresse.id AND prenom LIKE '%" + prenom + "'").fetchone()
    return jsonify({"prenom": reqPersonne["prenom"], "recherche entreprise": reqPersonne["rechercheEntreprise"], "ville": reqPersonne["ville"], "code postal": reqPersonne["codePostal"], "rue": reqPersonne["rue"], "numero rue": reqPersonne["numeroRue"]})
 
@app.route("/admin/entreprise/voir/<nom>", methods=["POST"])
@helper.verif_token
@helper.verif_root_entreprise
def voirEntreprise(nom) :
    reqEntreprise = bdd.execute("SELECT * FROM entreprise, adresse WHERE entreprise.idAdresse = adresse.id AND nom LIKE '%" + nom + "'").fetchone()
    return jsonify({"nom" : reqEntreprise["nom"], "recherche salarie" : reqEntreprise["rechercheSalarie"], "ville": reqEntreprise["ville"], "code postal": reqEntreprise["codePostal"], "rue": reqEntreprise["rue"], "numero rue": reqEntreprise["numeroRue"]})    

@app.route("/admin/personne/ajouter", methods=["PUT"])
@helper.verif_token
def ajouterPersonne() :
    data = request.form
    if "prenom" not in data or "rechercheEntreprise" not in data or "idAdresse" not in data or "motdepasse" not in data:
        return jsonify({"erreur": "Il manque des informations"})
    prenom = data["prenom"]
    rechercheEntreprise = data["rechercheEntreprise"]
    idAdresse = data["idAdresse"]
    motdepasse = data["motdepasse"]
    
    bdd.execute("INSERT INTO personne (prenom, rechercheEntreprise, idAdresse, motDePasse) VALUES ('" + prenom + "'," + rechercheEntreprise + ", " + idAdresse + ", '" + motdepasse + "')")
    bdd.commit()
    
    return (jsonify({"ajout": "reussi"}),201)

@app.route("/admin/personne/delete/<prenom>", methods=["DELETE"])
@helper.verif_token
@helper.verif_root_personne
def supprimerPersonne(prenom) :    
    #bdd.execute("DELETE FROM TABLE personne WHERE prenom LIKE '%'" + prenom + "'")
    #bdd.execute("commit")
    
    return jsonify({"suppression": True, "prenom": prenom})

if __name__ == '__main__':
    app.secret_key = 'pass'
    app.run()