import unittest
from api import app
from flask import json


class TestRoutePaulEmploi(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
    
    def test_connexion_vide(self) :
        response = self.app.get('/connexion')
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEquals(data['connexion'], "Les informations ne sont pas conformes")
        
    def test_connexion_personne(self) :
        response = self.app.get('/connexion', query_string={'identite': 'Lea', 'typeCompte': 'personne', "motdepasse": "motdepasse"})
        data = json.loads(response.data)
        self.assertEquals(data['connexion'], "reussi")
        
    def test_connexion_entreprise(self) :
        response = self.app.get('/connexion', query_string={'identite': 'Airbus', 'typeCompte': 'entreprise', "motdepasse": "motdepasse"})
        data = json.loads(response.data)
        self.assertEquals(data['connexion'], "reussi")
        
    def test_connexion_erreur(self) :
        responsePersonneInexistante = self.app.get('/connexion', query_string={'identite': 'Machin', 'typeCompte': 'personne', "motdepasse": "motdepasse"})
        responseEntrepriseInexistante = self.app.get('/connexion', query_string={'identite': 'Machin', 'typeCompte': 'entreprise', "motdepasse": "motdepasse"})
        responseTypeCompteInexistant = self.app.get('/connexion', query_string={'identite': 'Machin', 'typeCompte': 'nimportequoi', "motdepasse": "motdepasse"})
        responseMauvaisMotDePasse = self.app.get('/connexion', query_string={'identite': 'Lea', 'typeCompte': "personne", "motdepasse": "mauvaismotdepass"})
        
        dataPersonneInexistante = json.loads(responsePersonneInexistante.data)
        dataEntrepriseInexistante = json.loads(responseEntrepriseInexistante.data)
        dataTypeCompteInexistant = json.loads(responseTypeCompteInexistant.data)
        dataMauvaisMotDePasse = json.loads(responseMauvaisMotDePasse.data)
        
        jsonAttendu = "Les informations ne sont pas conformes"
        self.assertEquals(dataPersonneInexistante["connexion"], jsonAttendu)
        self.assertEquals(dataEntrepriseInexistante["connexion"], jsonAttendu)
        self.assertEquals(dataTypeCompteInexistant["connexion"], jsonAttendu)
        self.assertEquals(dataMauvaisMotDePasse["connexion"], jsonAttendu)
        
    def test_profil_mauvais_token(self) :
        response = self.app.post('/profil/Lea',data=dict(token='incorrectToken'))
        self.assertEquals(response.status_code, 200)
        data = json.loads(response.data)
        self.assertFalse(data['token'])
        
    def test_profil_personne(self) :
        responseLogin = self.app.get('/connexion', query_string={'identite': 'Lea', 'typeCompte': 'personne', "motdepasse": "motdepasse"})
        dataLogin = json.loads(responseLogin.data)
        token = dataLogin["token"]
        responseProfile = self.app.post('/profil/Lea', data=dict(token=token))
        dataProfile = json.loads(responseProfile.data)
        self.assertEquals(dataProfile, {"prenom": "Lea", "recherche entreprise": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "La residence", "numero rue": 31})
        
    def test_profil_entreprise(self) :
        responseLogin = self.app.get('/connexion', query_string={'identite': 'Airbus', 'typeCompte': 'entreprise', "motdepasse": "motdepasse"})
        dataLogin = json.loads(responseLogin.data)
        token = dataLogin["token"]
        responseProfile = self.app.post('/profil/Airbus', data=dict(token=token))
        dataProfile = json.loads(responseProfile.data)
        self.assertEquals(dataProfile, {"nom": "Airbus", "recherche salarie": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "Des caprices", "numero rue": 5})     
    
if __name__ == "__main__":
    app.secret_key = 'pass'
    unittest.main()