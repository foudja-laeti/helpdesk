from django.shortcuts import redirect
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch
import logging

# Configuration du logger pour le débogage si nécessaire
logger = logging.getLogger(__name__)


class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # --- 1. Fonction utilitaire pour récupérer les URLs de manière sûre ---

        def safe_reverse(name, default_path):
            """Tente de récupérer l'URL par nom, utilise un chemin par défaut si le nom n'existe pas."""
            try:
                # Tente de résoudre l'URL simple (e.g., 'login')
                url = reverse(name)
                # Assure que l'URL se termine par un slash pour la comparaison
                return url if url.endswith('/') else url + '/'
            except NoReverseMatch:
                try:
                    # Tente de résoudre l'URL avec un namespace (e.g., 'app_name:login')
                    # Remplacez 'app_name' par le namespace réel de votre app
                    # d'auth si besoin
                    url = reverse(f'auth:{name}')
                    return url if url.endswith('/') else url + '/'
                except NoReverseMatch:
                    # Retourne le chemin par défaut en dernier recours
                    return default_path if default_path.endswith(
                        '/') else default_path + '/'

        # --- 2. Définition des URLs de base ---

        # NOTE: Assurez-vous que 'login', 'register' et 'logout' sont bien les
        # noms dans vos urls.py
        login_url = safe_reverse('login', '/login/')
        register_url = safe_reverse('register', '/register/')
        logout_url = safe_reverse('logout', '/logout/')

        # URLs de réinitialisation de mot de passe
        password_reset_url = safe_reverse(
            'password_reset_request', '/password-reset/')

        # --- 3. Définition des URLs publiques (Accessibles sans connexion) ---

        # Seules ces pages sont accessibles si l'utilisateur n'est pas
        # connecté.
        public_urls = [
            login_url,      # Obligatoirement accessible
            register_url,   # Obligatoirement accessible
            logout_url,
            password_reset_url,  # ← AJOUT: Page de demande de reset
            '/admin/',
        ]

        # Normalisation du chemin de la requête
        request_path = request.path if request.path.endswith(
            '/') else request.path + '/'

        # Vérifie si le chemin actuel commence par une des URLs publiques
        is_public = any(request_path.startswith(url) for url in public_urls)

        # ← AJOUT: Autoriser TOUTES les URLs de reset password (avec les tokens)
        # Exemple: /password-reset-confirm/MQ/abc123/
        if request_path.startswith('/password-reset'):
            is_public = True

        # --- 4. Logique de vérification de connexion ---

        # Votre méthode de vérification de connexion
        user_is_logged_in = 'utilisateur_id' in request.session

        # CAS UNIQUE : Utilisateur est DÉCONNECTÉ et essaie d'accéder à une page PRIVÉE
        # Une page est privée si elle n'est pas dans la liste public_urls ET si
        # ce n'est pas un fichier statique
        if not user_is_logged_in and not is_public and not request_path.startswith(
                '/static/'):
            # Rediriger vers la page de connexion
            return redirect(login_url)

        # Poursuivre la requête normalement pour toutes les autres requêtes,
        # y compris pour les utilisateurs connectés sur /login/ ou /register/
        response = self.get_response(request)
        return response
