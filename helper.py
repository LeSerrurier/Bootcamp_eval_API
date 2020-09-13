import sqlite3
from functools import wraps
from flask import jsonify, request, session

bdd = sqlite3.connect('BDD/paulEmploi.db', check_same_thread=False)
bdd.row_factory = sqlite3.Row

def verif_token(f):
    @wraps(f)
    def decorator(*args, **kwargs): 
        data = request.form
        if "token" not in data :
            return jsonify({"token": False})
        token = data["token"]
        if token not in session :
           return jsonify({"token": False}) 
       
        session[token].update({"token": True})
        return f(*args, **kwargs)
    return decorator

def verif_root(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = request.form
        token = data["token"]

        if "root" != session[token]["identite"] :
            return jsonify({"erreur": "Vous n'avez pas les droits"})
        
        return f(*args, **kwargs)
    return decorator

def verif_root_personne(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = request.form
        token = data["token"]

        if "root" != session[token]["identite"] :
            return jsonify({"erreur": "Vous n'avez pas les droits"})
        
        prenom = kwargs["prenom"]
        verifExistant = bdd.execute("SELECT * FROM personne WHERE prenom LIKE '%" + prenom + "'").fetchone()
        if not verifExistant :
            return jsonify({"erreur": "Personne inexistante"})
        return f(*args, **kwargs)
    return decorator

def verif_root_entreprise(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        data = request.form
        token = data["token"]

        if "root" != session[token]["identite"] :
            return jsonify({"erreur": "Vous n'avez pas les droits"})
        
        nom = kwargs["nom"]        
        verifExistant = bdd.execute("SELECT * FROM entreprise WHERE nom LIKE '%" + nom + "'").fetchone()
        if not verifExistant :
            return jsonify({"erreur": "Entreprise inexistante"})
        
        return f(*args, **kwargs)
    return decorator

