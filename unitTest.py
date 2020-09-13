import unittest, sys
sys.path.insert(1, "BDD/")
from createBDD import *
from deleteBDD import *
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
        reponseProfil = self.app.post('/profil/Lea', data=dict(token=self.token))
        dataProfil = json.loads(reponseProfil.data)
        self.assertEquals(dataProfil, {"prenom": "Lea", "recherche entreprise": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "La residence", "numero rue": 31})
        
    def test_profil_mauvaise_personne(self) :
        reponseProfil = self.app.post('/profil/Paul', data=dict(token=self.token))
        dataProfil = json.loads(reponseProfil.data)
        self.assertEquals(dataProfil, {"erreur": "Ce n'est pas votre compte"})
        
    def test_personne_recherche_entreprise(self) :
        reponseRecherche = self.app.post("/recherche/entreprise", data=dict(token=self.token))
        dataRecherche = json.loads(reponseRecherche.data)
        self.assertEquals(dataRecherche, {"entreprise 1" : {"nom" : "Airbus", "ville": "Toulouse", "code postal": 31200, "rue": "Des caprices", "numero rue": 5},
                                          "entreprise 2" : {"nom" : "CapGemini","ville": "Tournefeuille", "code postal": 31170, "rue": "Des chats", "numero rue": 45}})     
   
    def test_recherche_personne_pas_acces(self) :
        reponseRecherche = self.app.post('/recherche/personne', data=dict(token=self.token))
        dataRecherche = json.loads(reponseRecherche.data)
        self.assertEquals(dataRecherche["erreur"], "Vous n'avez pas acces a cette partie")
        
    def test_voir_salarie_entreprise_pas_acces(self) :
        reponseVoir = self.app.post('/entreprise/salarie', data=dict(token=self.token))
        dataVoir = json.loads(reponseVoir.data)
        self.assertEquals(dataVoir["erreur"], "Vous n'avez pas acces a cette partie")
    
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
        reponseProfil = self.app.post('/profil/Airbus', data=dict(token=self.token))
        dataProfil = json.loads(reponseProfil.data)
        self.assertEquals(dataProfil, {"nom": "Airbus", "recherche salarie": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "Des caprices", "numero rue": 5})     

    def test_recherche_personne(self) :
        reponseRecherche = self.app.post('/recherche/personne', data=dict(token=self.token))
        dataRecherche = json.loads(reponseRecherche.data)
        self.assertEquals(dataRecherche, {"personne 1" : {"prenom" : "Paul", "ville": "Toulouse", "code postal": 31200, "rue": "La residence", "numero rue": 31},
                                          "personne 2" : {"prenom" : "Gerard", "ville": "Toulouse", "code postal": 31200, "rue": "La residence", "numero rue": 31},
                                          "personne 3" : {"prenom" : "Lea", "ville": "Toulouse", "code postal": 31200, "rue": "La residence", "numero rue": 31}})
    
    def test_recherche_entreprise_pas_acces(self) :
        reponseRecherche = self.app.post('/recherche/entreprise', data=dict(token=self.token))
        dataRecherche = json.loads(reponseRecherche.data)
        self.assertEquals(dataRecherche["erreur"], "Vous n'avez pas acces a cette partie")
        
    def test_voir_ses_salaries(self) :
        reponseVoir = self.app.post('/entreprise/salarie', data=dict(token=self.token))
        dataVoir = json.loads(reponseVoir.data)
        self.assertEquals(dataVoir, {"salarie 1": {"prenom": "Anthony"}, "salarie 2": {"prenom": "Toto"}})
    
class TestRouteRoot(unittest.TestCase) :
    def setUp(self):
        self.app = app.test_client()
        reponseLogin = self.app.get('/connexion', query_string={'identite': 'root', 'typeCompte': 'personne', "motdepasse": "root"})
        dataLogin = json.loads(reponseLogin.data)
        self.token = dataLogin["token"]
        
    def tearDown(self) :
        supprimerBDD()
        creerBDD()
        
    def test_root_voir_profil_personne(self) :
        reponseVoir = self.app.post('/admin/personne/voir/Lea', data=dict(token=self.token))
        self.assertEquals(reponseVoir.status_code, 200)
        data = json.loads(reponseVoir.data)
        self.assertEquals(data, {"prenom": "Lea", "recherche entreprise": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "La residence", "numero rue": 31})
        
    def test_root_voir_profil_inexistant(self) :
        reponseVoirPersonne = self.app.post('/admin/personne/voir/Dupont', data=dict(token=self.token))
        reponseVoirEntreprise = self.app.post('/admin/entreprise/voir/Inc', data=dict(token=self.token))
        
        dataPersonne = json.loads(reponseVoirPersonne.data)
        dataEntreprise = json.loads(reponseVoirEntreprise.data)
        
        self.assertEquals(dataPersonne, {"erreur": "Personne inexistante"})
        self.assertEquals(dataEntreprise, {"erreur": "Entreprise inexistante"})
        
    def test_root_voir_profil_mauvais_compte(self) :
        reponseLogin = self.app.get('/connexion', query_string={'identite': 'Lea', 'typeCompte': 'personne', "motdepasse": "motdepasse"})
        dataLogin = json.loads(reponseLogin.data)
        self.token = dataLogin["token"]
        reponseVoir = self.app.post('/admin/personne/voir/Lea', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data, {"erreur": "Vous n'avez pas les droits"})
        
    def test_root_voir_profil_entreprise(self) :
        reponseVoir = self.app.post('/admin/entreprise/voir/Airbus', data=dict(token=self.token))
        self.assertEquals(reponseVoir.status_code, 200)
        data = json.loads(reponseVoir.data)
        self.assertEquals(data, {"nom": "Airbus", "recherche salarie": 1,
                                        "ville": "Toulouse", "code postal": 31200, "rue": "Des caprices", "numero rue": 5})     

    def test_root_ajouter_personne(self) :
        reponseAjouter = self.app.post('/admin/personne/ajouter', data=dict(token=self.token, prenom="Pierre", rechercheEntreprise=0, idAdresse=4, motdepasse="motdepasse"))
        self.assertEquals(reponseAjouter.status_code, 201)
        data = json.loads(reponseAjouter.data)
        self.assertEquals(data, {"ajout": "reussi"})
        reponseVoir = self.app.post('/admin/personne/voir/Pierre', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data["prenom"], "Pierre")
        
    def test_root_ajouter_entreprise(self) :
        reponseAjouter = self.app.post('/admin/entreprise/ajouter', data=dict(token=self.token, nom="CIC", rechercheSalarie=0, idAdresse=3, motdepasse="motdepasse"))
        self.assertEquals(reponseAjouter.status_code, 201)
        data = json.loads(reponseAjouter.data)
        self.assertEquals(data, {"ajout": "reussi"})
        reponseVoir = self.app.post('/admin/entreprise/voir/CIC', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data["nom"], "CIC")
        
    def test_root_suppression_personne(self) :
        reponseDelete = self.app.delete('/admin/personne/delete/Lea', data=dict(token=self.token))
        self.assertEquals(reponseDelete.status_code, 200)
        data = json.loads(reponseDelete.data)
        self.assertEquals(data, {"suppression": 1, "prenom": "Lea"})
        reponseVoir = self.app.post('/admin/personne/voir/Lea', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data["erreur"], "Personne inexistante")
    
    def test_root_suppression_entreprise(self) :
        reponseDelete = self.app.delete('/admin/entreprise/delete/Airbus', data=dict(token=self.token))
        self.assertEquals(reponseDelete.status_code, 200)
        data = json.loads(reponseDelete.data)
        self.assertEquals(data, {"suppression": 1, "nom": "Airbus"})
        reponseVoir = self.app.post('/admin/entreprise/voir/Airbus', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data["erreur"], "Entreprise inexistante")
        
    def test_root_update_un_champ_personne(self) :
        reponseUpdate = self.app.put('/admin/personne/update/Lea', data=dict(token=self.token, prenom="Leanna"))
        self.assertEquals(reponseUpdate.status_code, 200)
        data = json.loads(reponseUpdate.data)
        self.assertEquals(data, {"mise a jour 1": {"statut" : "reussi", "ancien prenom": "Lea", "nouveau prenom": "Leanna"}})
        reponseVoir = self.app.post('/admin/personne/voir/Leanna', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data["prenom"], "Leanna")
        reponseVoir = self.app.post('/admin/personne/voir/Lea', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data["erreur"], "Personne inexistante")
        
        reponseUpdate = self.app.put('/admin/personne/update/Leanna', data=dict(token = self.token, rechercheEntreprise = 0))
        data = json.loads(reponseUpdate.data)
        self.assertEquals(data, {"mise a jour 1": {"statut": "reussi", "ancien rechercheEntreprise": "1", "nouveau rechercheEntreprise": '0'}})
        reponseVoir = self.app.post('/admin/personne/voir/Leanna', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data["recherche entreprise"], 0)
        
    def test_root_update_plusieurs_champ_personne(self) :
        reponseUpdate = self.app.put('/admin/personne/update/Lea', data=dict(token = self.token, rechercheEntreprise = 0, idAdresse = 1))
        data = json.loads(reponseUpdate.data)
        self.assertEquals(data, {"mise a jour 2": {"statut" : "reussi", "ancien rechercheEntreprise": '1', "nouveau rechercheEntreprise": '0'},
                                 "mise a jour 1": {"statut" : "reussi", "ancien idAdresse": '4', "nouveau idAdresse": '1'}})
        reponseVoir = self.app.post('/admin/personne/voir/Lea', data=dict(token=self.token))
        data = json.loads(reponseVoir.data)
        self.assertEquals(data, {"prenom": "Lea", "recherche entreprise": 0,
                                 "ville": "Toulouse", "code postal": 31200, "rue": "Des caprices", "numero rue": 5})

        
if __name__ == "__main__":
    app.secret_key = 'pass'
    unittest.main()