import unittest
from api import app
from flask import json


class TestRoutePersonne(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        reponseLogin = self.app.get('/connexion', query_string={'identite': 'Lea', 'typeCompte': 'personne', "motdepasse": "motdepasse"})
        dataLogin = json.loads(reponseLogin.data)
        self.token = dataLogin["token"]
    
    def test_connexion_vide(self) :
        reponse = self.app.get('/connexion')
        self.assertEquals(reponse.status_code, 200)
        data = json.loads(reponse.data)
        self.assertEquals(data['connexion'], "Les informations ne sont pas conformes")
        
    def test_connexion_personne(self) :
        reponse = self.app.get('/connexion', query_string={'identite': 'Lea', 'typeCompte': 'personne', "motdepasse": "motdepasse"})
        data = json.loads(reponse.data)
        self.assertEquals(data['connexion'], "reussi")
        
    def test_connexion_erreur(self) :
        reponsePersonneInexistante = self.app.get('/connexion', query_string={'identite': 'Machin', 'typeCompte': 'personne', "motdepasse": "motdepasse"})
        reponseEntrepriseInexistante = self.app.get('/connexion', query_string={'identite': 'Machin', 'typeCompte': 'entreprise', "motdepasse": "motdepasse"})
        reponseTypeCompteInexistant = self.app.get('/connexion', query_string={'identite': 'Machin', 'typeCompte': 'nimportequoi', "motdepasse": "motdepasse"})
        reponseMauvaisMotDePasse = self.app.get('/connexion', query_string={'identite': 'Lea', 'typeCompte': "personne", "motdepasse": "mauvaismotdepass"})
        
        dataPersonneInexistante = json.loads(reponsePersonneInexistante.data)
        dataEntrepriseInexistante = json.loads(reponseEntrepriseInexistante.data)
        dataTypeCompteInexistant = json.loads(reponseTypeCompteInexistant.data)
        dataMauvaisMotDePasse = json.loads(reponseMauvaisMotDePasse.data)
        
        jsonAttendu = "Les informations ne sont pas conformes"
        self.assertEquals(dataPersonneInexistante["connexion"], jsonAttendu)
        self.assertEquals(dataEntrepriseInexistante["connexion"], jsonAttendu)
        self.assertEquals(dataTypeCompteInexistant["connexion"], jsonAttendu)
        self.assertEquals(dataMauvaisMotDePasse["connexion"], jsonAttendu)
        
    def test_profil_mauvais_token(self) :
        reponse = self.app.post('/profil/Lea',data=dict(token='incorrectToken'))
        self.assertEquals(reponse.status_code, 200)
        data = json.loads(reponse.data)
        self.assertFalse(data['token'])
        
    def test_profil_personne(self) :
        reponseProfile = self.app.post('/profil/Lea', data=dict(token=self.token))
        dataProfile = json.loads(reponseProfile.data)
        self.assertEquals(dataProfile, {"prenom": "Lea", "recherche entreprise": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "La residence", "numero rue": 31})
        
    def test_profil_mauvaise_personne(self) :
        reponseProfile = self.app.post('/profil/Paul', data=dict(token=self.token))
        dataProfile = json.loads(reponseProfile.data)
        self.assertEquals(dataProfile, {"erreur": "Ce n'est pas votre compte"})
    
    
class TestRouteEntreprise(unittest.TestCase) :
        
    def setUp(self):
        self.app = app.test_client()
        reponseLogin = self.app.get('/connexion', query_string={'identite': 'Airbus', 'typeCompte': 'entreprise', "motdepasse": "motdepasse"})
        dataLogin = json.loads(reponseLogin.data)
        self.token = dataLogin["token"]
    
    def test_connexion_entreprise(self) :
        reponse = self.app.get('/connexion', query_string={'identite': 'Airbus', 'typeCompte': 'entreprise', "motdepasse": "motdepasse"})
        data = json.loads(reponse.data)
        self.assertEquals(data['connexion'], "reussi")
    
    def test_profil_entreprise(self) :
        reponseProfile = self.app.post('/profil/Airbus', data=dict(token=self.token))
        dataProfile = json.loads(reponseProfile.data)
        self.assertEquals(dataProfile, {"nom": "Airbus", "recherche salarie": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "Des caprices", "numero rue": 5})     

    
class TestRouteRoot(unittest.TestCase) :
    
    def setUp(self):
        self.app = app.test_client()
        reponseLogin = self.app.get('/connexion', query_string={'identite': 'root', 'typeCompte': 'personne', "motdepasse": "root"})
        dataLogin = json.loads(reponseLogin.data)
        self.token = dataLogin["token"]
        
    def test_root_voir_profil_personne(self) :
        reponseVoir = self.app.get('/admin/personne/voir/Lea')
        self.assertEquals(reponseVoir.status_code, 200)
        data = json.loads(reponseVoir.data)
        self.assertEquals(data, {"prenom": "Lea", "recherche entreprise": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "La residence", "numero rue": 31})
        
    def test_root_voir_profil_inexistant(self) :
        reponseVoir = self.app.get('/admin/personne/voir/Dupont')
        self.assertEquals(reponseVoir.status_code, 200)
        data = json.loads(reponseVoir.data)
        self.assertEquals(data, {"erreur": "Personne inexistante"})
    
    def test_root_suppression_personne(self) :
        reponseDelete = self.app.delete('/admin/personne/delete/Lea', data=dict(token=self.token))
        self.assertEquals(reponseDelete.status_code, 200)
        data = json.loads(reponseDelete.data)
        self.assertEquals(data, {"suppression": 1, "prenom": "Lea"})
        
        #reponseVerifSuppression = self.app.get("/profil/Lea")
        #self.assertEquals(reponseVerifSupression)
   
    
if __name__ == "__main__":
    app.secret_key = 'pass'
    unittest.main()