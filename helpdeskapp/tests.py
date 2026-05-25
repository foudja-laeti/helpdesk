from django.test import TestCase, RequestFactory
from django.contrib.auth.hashers import make_password
from helpdeskapp.models import Utilisateur, Domaine, Demande
from helpdeskapp.forms import DomaineForm, UtilisateurForm, DemandeForm, LoginForm
from helpdeskapp.views import extract_city_from_address, get_weather_data


# ==================== TESTS MODÈLES ====================

class UtilisateurModelTest(TestCase):

    def setUp(self):
        self.utilisateur = Utilisateur.objects.create(
            nom="Dupont",
            prenom="Jean",
            telephone="699000001",
            adresse="Douala, Akwa",
            email="jean@test.com",
            password=make_password("motdepasse123"),
            role="client"
        )

    def test_creation_utilisateur(self):
        self.assertEqual(self.utilisateur.nom, "Dupont")
        self.assertEqual(self.utilisateur.role, "client")

    def test_str_utilisateur(self):
        self.assertEqual(str(self.utilisateur), "Dupont Jean (client)")

    def test_roles_valides(self):
        roles = [r[0] for r in Utilisateur.ROLES]
        self.assertIn("client", roles)
        self.assertIn("technicien", roles)
        self.assertIn("administrateur", roles)


class DomaineModelTest(TestCase):

    def setUp(self):
        self.domaine = Domaine.objects.create(
            intitule="Réseau",
            description="Problèmes réseau et connectivité"
        )

    def test_creation_domaine(self):
        self.assertEqual(self.domaine.intitule, "Réseau")

    def test_str_domaine(self):
        self.assertEqual(str(self.domaine), "Réseau")


class DemandeModelTest(TestCase):

    def setUp(self):
        self.client_user = Utilisateur.objects.create(
            nom="Client", prenom="Test", telephone="600000001",
            adresse="Douala", email="client@test.com",
            password=make_password("pass"), role="client"
        )
        self.technicien = Utilisateur.objects.create(
            nom="Tech", prenom="Test", telephone="600000002",
            adresse="Douala", email="tech@test.com",
            password=make_password("pass"), role="technicien"
        )
        self.domaine = Domaine.objects.create(
            intitule="Matériel", description="Pannes matérielles"
        )
        self.demande = Demande.objects.create(
            client=self.client_user,
            technicien=self.technicien,
            domaine=self.domaine,
            intitule="Écran cassé",
            description="L'écran ne s'allume plus",
            statut="en attente",
            adresse="Douala, Bonapriso"
        )

    def test_creation_demande(self):
        self.assertEqual(self.demande.intitule, "Écran cassé")
        self.assertEqual(self.demande.statut, "en attente")

    def test_str_demande(self):
        self.assertEqual(str(self.demande), "Écran cassé (en attente)")

    def test_statut_defaut(self):
        demande = Demande.objects.create(
            client=self.client_user,
            domaine=self.domaine,
            intitule="Test statut",
            description="desc"
        )
        self.assertEqual(demande.statut, "en attente")


# ==================== TESTS FORMULAIRES ====================

class DomaineFormTest(TestCase):

    def test_form_valide(self):
        form = DomaineForm(data={"intitule": "Logiciel", "description": "Bugs logiciels"})
        self.assertTrue(form.is_valid())

    def test_form_invalide_champs_vides(self):
        form = DomaineForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn("intitule", form.errors)


class UtilisateurFormTest(TestCase):

    def test_form_valide(self):
        form = UtilisateurForm(data={
            "nom": "Kamga", "prenom": "Paul",
            "telephone": "677000001", "adresse": "Yaoundé",
            "email": "kamga@test.com", "password": "secure123",
            "role": "client"
        })
        self.assertTrue(form.is_valid())

    def test_form_email_invalide(self):
        form = UtilisateurForm(data={
            "nom": "Kamga", "prenom": "Paul",
            "telephone": "677000001", "adresse": "Yaoundé",
            "email": "pas-un-email", "password": "secure123",
            "role": "client"
        })
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)


class LoginFormTest(TestCase):

    def test_form_valide(self):
        form = LoginForm(data={"email": "user@test.com", "password": "pass123"})
        self.assertTrue(form.is_valid())

    def test_form_invalide_sans_email(self):
        form = LoginForm(data={"email": "", "password": "pass123"})
        self.assertFalse(form.is_valid())


# ==================== TESTS VUES (UTILITAIRES) ====================

class ExtractCityTest(TestCase):

    def test_adresse_avec_virgule(self):
        self.assertEqual(extract_city_from_address("Douala, Akwa"), "Douala")

    def test_adresse_sans_virgule(self):
        self.assertEqual(extract_city_from_address("Yaoundé"), "Yaoundé")

    def test_adresse_vide(self):
        self.assertEqual(extract_city_from_address(""), "Douala")

    def test_adresse_none(self):
        self.assertEqual(extract_city_from_address(None), "Douala")

    def test_adresse_yaoundé_avec_quartier(self):
        self.assertEqual(extract_city_from_address("Yaoundé, Bastos"), "Yaoundé")


class GetWeatherDataTest(TestCase):

    def test_retour_sans_cle_api(self):
        """Sans clé API valide, doit retourner les données de fallback."""
        result = get_weather_data("Douala")
        self.assertTrue(result["success"])
        self.assertIn("temperature", result)
        self.assertIn("city", result)

    def test_retour_ville_inconnue(self):
        result = get_weather_data("VilleInexistante123")
        self.assertTrue(result["success"])