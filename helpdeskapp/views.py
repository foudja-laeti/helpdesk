from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import requests 
from django.contrib.auth.hashers import make_password, check_password
from .models import *
import logging

from .forms import *
from django.db.models import Q 

#Creaion du logger pour l'application helpdeskapp
logger = logging.getLogger('helpdeskapp')

# ==================== GESTION DES DOMAINES ====================

def list_domaines(request):
    """Affiche la liste de tous les domaines."""
    # Cette page est la destination par défaut après la connexion
    if 'utilisateur_id' not in request.session:
        return redirect('login')
        
    domaines = Domaine.objects.all()
    return render(request, 'domaine/list.html', {'domaines': domaines})

def add_domaines(request):
    """Ajoute un nouveau domaine."""
    form = DomaineForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Le domaine ajouté avec succès !!')
            return redirect('domaine:list_domaines')
        else:
            messages.error(request, 'Erreur lors de l\'ajout du domaine')
    return render(request, 'domaine/form.html', {'form': form})

def update_domaines(request, id):
    """Modifie un domaine existant."""
    domaine = get_object_or_404(Domaine, id=id)
    form = DomaineForm(request.POST or None, instance=domaine)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Le domaine a été modifié avec succès !!')
            return redirect('domaine:list_domaines')
        else:
            messages.error(request, 'Erreur lors de la modification du domaine')
    return render(request, 'domaine/form.html', {'form': form, 'domaine': domaine})

def delete_domaines(request, id):
    """Supprime un domaine."""
    domaine = get_object_or_404(Domaine, id=id)
    if domaine is not None and domaine.id > 0:
        domaine.delete()
        messages.success(request, 'Le domaine a été supprimé avec succès !!')
    else:
        messages.error(request, 'Erreur lors de la suppression du domaine')
    return redirect('domaine:list_domaines')


# ==================== GESTION DES UTILISATEURS ====================

def list_utilisateurs(request):
    """Affiche la liste de tous les utilisateurs."""
    utilisateurs = Utilisateur.objects.all()
    return render(request, 'utilisateur/list.html', {'utilisateurs': utilisateurs})


def add_utilisateur(request):
    """Ajoute un nouvel utilisateur (utilisé par l'administrateur)."""
    form = UtilisateurForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            utilisateur = form.save(commit=False)
            # Hacher le mot de passe avant de sauvegarder
            utilisateur.password = make_password(form.cleaned_data['password'])
            utilisateur.save()
            messages.success(request, 'L\'utilisateur a été ajouté avec succès !!')
            return redirect('utilisateur:list_utilisateurs')
        else:
            messages.error(request, 'Erreur lors de l\'ajout de l\'utilisateur')
    return render(request, 'utilisateur/form.html', {'form': form})


def update_utilisateur(request, id):
    """Modifie un utilisateur existant."""
    utilisateur = get_object_or_404(Utilisateur, id=id)
    form = UtilisateurForm(request.POST or None, instance=utilisateur)
    if request.method == 'POST':
        if form.is_valid():
            utilisateur = form.save(commit=False)
            # Ne hacher le mot de passe que s'il a été modifié
            if 'password' in form.changed_data:
                utilisateur.password = make_password(form.cleaned_data['password'])
            utilisateur.save()
            messages.success(request, 'L\'utilisateur a été modifié avec succès !!')
            return redirect('utilisateur:list_utilisateurs')
        else:
            messages.error(request, 'Erreur lors de la modification de l\'utilisateur')
    return render(request, 'utilisateur/form.html', {'form': form, 'utilisateur': utilisateur})



def delete_utilisateur(request, id):
    """Supprime un utilisateur."""
    utilisateur = get_object_or_404(Utilisateur, id=id)
    if utilisateur is not None and utilisateur.id > 0:
        utilisateur.delete()
        messages.success(request, 'L\'utilisateur a été supprimé avec succès !!')
    else:
        messages.error(request, 'Erreur lors de la suppression de l\'utilisateur')
    return redirect('utilisateur:list_utilisateurs')


def detail_utilisateur(request, id):
    """Affiche les détails d'un utilisateur."""
    utilisateur = get_object_or_404(Utilisateur, id=id)
    return render(request, 'utilisateur/detail.html', {'utilisateur': utilisateur})


def list_utilisateurs_by_role(request, role):
    """Affiche les utilisateurs filtrés par rôle."""
    utilisateurs = Utilisateur.objects.filter(role=role)
    return render(request, 'utilisateur/list.html', {
        'utilisateurs': utilisateurs,
        'role_filtre': role
    })


def search_utilisateurs(request):
    """Effectue une recherche d'utilisateurs par nom, prénom ou email."""
    query = request.GET.get('q', '')
    if query:
        # Utilisation de Q pour combiner les filtres avec OR (§§|§)
        utilisateurs = Utilisateur.objects.filter(
            Q(nom__icontains=query) |
            Q(prenom__icontains=query) |
            Q(email__icontains=query)
        )
    else:
        utilisateurs = Utilisateur.objects.all()
    return render(request, 'utilisateur/list.html', {'utilisateurs': utilisateurs, 'query': query})


# ==================== GESTION DES DEMANDES ====================
def extract_city_from_address(address):
    """
    Extrait le nom de la ville d'une adresse.
    Exemples:
    - "Douala, Akwa" -> "Douala"
    - "Yaoundé, Bastos" -> "Yaoundé"
    - "Bonaberi" -> "Bonaberi"
    """
    if not address:
        return "Douala"  # Ville par défaut
    
    address = address.strip()
    
    if ',' in address:
        city = address.split(',')[0].strip()
    else:
        city = address.split()[0].strip()
    
    return city if city else "Douala"


def get_weather_data(city="Douala"):
    """
    Récupère les données météo avec fallback sur données factices.
    """
    try:
        API_KEY = getattr(settings, 'OPENWEATHER_API_KEY', '')
        
        # Si pas de clé ou clé invalide, utiliser données factices
        if not API_KEY or API_KEY == 'votre_api_key_ici':
            logger.info(f"Pas de clé API - Utilisation données factices pour {city}")
            return {
                'city': city,
                'temperature': 28,
                'description': 'Partiellement nuageux',
                'humidity': 78,
                'wind_speed': 14.5,
                'icon': '02d',
                'feels_like': 31,
                'success': True,
                'is_fallback': True
            }
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric',
            'lang': 'fr'
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            
            weather_info = {
                'city': data['name'],
                'temperature': round(data['main']['temp']),
                'description': data['weather'][0]['description'].capitalize(),
                'humidity': data['main']['humidity'],
                'wind_speed': round(data['wind']['speed'] * 3.6, 1),
                'icon': data['weather'][0]['icon'],
                'feels_like': round(data['main']['feels_like']),
                'success': True
            }
            
            logger.info(f"Données météo API récupérées pour {city}")
            return weather_info
        else:
            # Fallback automatique
            logger.warning(f"API météo erreur {response.status_code} - Fallback données factices")
            return {
                'city': city,
                'temperature': 28,
                'description': 'Partiellement nuageux',
                'humidity': 78,
                'wind_speed': 14.5,
                'icon': '02d',
                'feels_like': 31,
                'success': True,
                'is_fallback': True
            }
            
    except Exception as e:
        logger.warning(f"Erreur météo: {str(e)} - Fallback données factices")
        return {
            'city': city,
            'temperature': 28,
            'description': 'Partiellement nuageux',
            'humidity': 78,
            'wind_speed': 14.5,
            'icon': '02d',
            'feels_like': 31,
            'success': True,
            'is_fallback': True
        }

def list_demandes(request):
    """Affiche la liste de toutes les demandes avec météo par adresse."""
    demandes = Demande.objects.all().order_by('-datedemande')
    
    # ⭐ Ajouter les données météo pour chaque demande
    demandes_avec_meteo = []
    for demande in demandes:
        # Extraire la ville de l'adresse
        ville = extract_city_from_address(demande.adresse)
        
        # Récupérer la météo pour cette ville
        meteo = get_weather_data(ville)
        
        demandes_avec_meteo.append({
            'demande': demande,
            'meteo': meteo,
            'ville': ville
        })
    
    return render(request, 'demande/list.html', {
        'demandes_avec_meteo': demandes_avec_meteo
    })
def add_demande(request):
    """Ajoute une nouvelle demande."""
    form = DemandeForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            demande = form.save()  # ⭐ Récupérer l'objet sauvegardé
            
            # ⭐ Récupérer l'ID de l'utilisateur depuis la session
            utilisateur_id = request.session.get('utilisateur_id', 'Inconnu')
            
            logger.info(f"Nouvelle demande ajoutée par l'utilisateur ID: {utilisateur_id}, Demande ID: {demande.id}")
            messages.success(request, 'La demande a été ajoutée avec succès !')
            return redirect('demande:list_demandes')
        else:
            # ⭐ Récupérer l'ID de l'utilisateur pour le log d'erreur
            utilisateur_id = request.session.get('utilisateur_id', 'Inconnu')
            
            logger.warning(f"Erreur lors de l'ajout de la demande par l'utilisateur ID: {utilisateur_id}")
            messages.error(request, 'Erreur lors de l\'ajout de la demande. Veuillez vérifier les informations.')

    return render(request, 'demande/form.html', {'form': form, 'action': 'Ajouter'})

def update_demande(request, id):
    """Modifie une demande existante."""
    demande = get_object_or_404(Demande, id=id)
    form = DemandeForm(request.POST or None, instance=demande)


    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'La demande a été modifiée avec succès !')
            return redirect('demande:list_demandes')
        else:
            messages.error(request, 'Erreur lors de la modification de la demande. Veuillez vérifier les informations.')


    return render(request, 'demande/form.html', {'form': form, 'demande': demande, 'action': 'Modifier'})



def delete_demande(request, id):
    """Supprime une demande."""
    demande = get_object_or_404(Demande, id=id)
    nom_demande = demande.intitule


    demande.delete()
    messages.success(request, f'La demande "{nom_demande}" a été supprimée avec succès !')
    return redirect('demande:list_demandes')



def detail_demande(request, id):
    """Affiche les détails d'une demande."""
    demande = get_object_or_404(Demande, id=id)
    return render(request, 'demande/detail.html', {'demande': demande})


# ==================== AUTHENTIFICATION ====================


def login_view(request):
    """Gère la connexion de l'utilisateur"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        utilisateur = Utilisateur.objects.filter(email=email).first()

        if utilisateur and check_password(password, utilisateur.password):
            request.session['utilisateur_id'] = utilisateur.id
            request.session['utilisateur_nom'] = utilisateur.nom
            request.session['utilisateur_prenom'] = utilisateur.prenom
            request.session['utilisateur_role'] = utilisateur.role


            logger.info(f"utilisateur connecté: {utilisateur.nom} (ID: {utilisateur.id}), (Role: {utilisateur.role})")
            messages.success(request, f'Bienvenue {utilisateur.nom} {utilisateur.prenom} !')

            # CORRECTION: Tous les rôles vont maintenant vers 'dashboard'
            # qui va rediriger automatiquement vers le bon dashboard
            return redirect('dashboard')
        else:
            logger.warning(f"echec de connexion pour l'email: {email}")
            messages.error(request, 'Email ou mot de passe incorrect.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    """
    Gère la déconnexion de l'utilisateur.
    """
    request.session.flush()
    messages.success(request, 'Vous êtes déconnecté.')
    return redirect('login')


def register_view(request):
    """
    Gère l'inscription de l'utilisateur.
    REDIRECTION : Succès -> 'login'
    """
    # L'utilisateur PEUT accéder à cette page même s'il est déjà connecté (selon votre exigence).
    # Suppression de la redirection 'home' pour les utilisateurs connectés.
        
    form = UtilisateurForm(request.POST or None)
    
    if request.method == 'POST':
        if form.is_valid():
            utilisateur = form.save(commit=False)
            
            # Hacher le mot de passe avant de sauvegarder
            utilisateur.password = make_password(form.cleaned_data['password'])
            utilisateur.save()
            
            messages.success(request, "Inscription réussie ! Veuillez vous connecter.")
            
            # Point de redirection CLÉ 2: Après inscription réussie, va à 'login'
            return redirect('login')
        else:
            messages.error(request, "Erreur lors de l'inscription. Veuillez vérifier les champs.")
            
    # Affichage du formulaire
    return render(request, 'accounts/register.html', {'form': form})

# Ajoutez ces fonctions à votre views.py existant

def dashboard_view(request):
    """Redirige vers le dashboard approprié selon le rôle"""
    if 'utilisateur_role' not in request.session:
        return redirect('login')
    
    role = request.session['utilisateur_role']
    
    if role == 'administrateur':
        return redirect('dashboard_admin')
    elif role == 'technicien':
        return redirect('dashboard_technicien')
    elif role == 'client':
        return redirect('dashboard_client')
    else:
        return redirect('login')


def dashboard_admin(request):
    """Dashboard pour l'administrateur - AVEC MÉTÉO"""
    if 'utilisateur_role' not in request.session or request.session['utilisateur_role'] != 'administrateur':
        return redirect('login')
    
    # Statistiques pour l'admin
    total_clients = Utilisateur.objects.filter(role='client').count()
    total_techniciens = Utilisateur.objects.filter(role='technicien').count()
    total_demandes = Demande.objects.count()
    demandes_en_attente = Demande.objects.filter(statut='en attente').count()
    demandes_en_cours = Demande.objects.filter(statut='en cours').count()
    total_domaines = Domaine.objects.count()
    
    # Activités récentes
    dernieres_demandes = Demande.objects.all().order_by('-datedemande')[:5]
    
    # ⭐ AJOUT DE LA MÉTÉO ⭐
    ville = "Douala"  # Ville par défaut
    weather_data = get_weather_data(ville)
    
    context = {
        'total_clients': total_clients,
        'total_techniciens': total_techniciens,
        'total_demandes': total_demandes,
        'demandes_en_attente': demandes_en_attente,
        'demandes_en_cours': demandes_en_cours,
        'total_domaines': total_domaines,
        'dernieres_demandes': dernieres_demandes,
        'weather': weather_data,  
    }
    
    return render(request, 'dashboard/admin_dashboard.html', context)

def dashboard_technicien(request):
    """Dashboard pour le technicien - AVEC MÉTÉO"""
    if 'utilisateur_role' not in request.session or request.session['utilisateur_role'] != 'technicien':
        return redirect('login')
    
    utilisateur_id = request.session.get('utilisateur_id')
    technicien = get_object_or_404(Utilisateur, id=utilisateur_id)
    
    # Statistiques pour le technicien
    mes_demandes = Demande.objects.filter(technicien=technicien)
    total_demandes = mes_demandes.count()
    demandes_en_attente = mes_demandes.filter(statut='en attente').count()
    demandes_en_cours = mes_demandes.filter(statut='en cours').count()
    demandes_terminees = mes_demandes.filter(statut='terminée').count()
    
    demandes_recentes = mes_demandes.order_by('-datedemande')[:5]
    demandes_urgentes = mes_demandes.filter(statut='en attente').order_by('-datedemande')[:3]
    
    # ⭐ AJOUT DE LA MÉTÉO ⭐
    ville = "Douala"  # Ville par défaut
    weather_data = get_weather_data(ville)
    
    context = {
        'technicien': technicien,
        'total_demandes': total_demandes,
        'demandes_en_attente': demandes_en_attente,
        'demandes_en_cours': demandes_en_cours,
        'demandes_terminees': demandes_terminees,
        'demandes_recentes': demandes_recentes,
        'demandes_urgentes': demandes_urgentes,
        'weather': weather_data,  # ⭐ Ajout de la météo dans le contexte
    }
    
    return render(request, 'dashboard/technicien_dashboard.html', context)

def dashboard_client(request):
    """Dashboard pour le client - AVEC MÉTÉO"""
    if 'utilisateur_role' not in request.session or request.session['utilisateur_role'] != 'client':
        return redirect('login')
    
    utilisateur_id = request.session.get('utilisateur_id')
    client = get_object_or_404(Utilisateur, id=utilisateur_id)
    
    # Statistiques pour le client
    mes_demandes = Demande.objects.filter(client=client)
    total_demandes = mes_demandes.count()
    demandes_en_attente = mes_demandes.filter(statut='en attente').count()
    demandes_en_cours = mes_demandes.filter(statut='en cours').count()
    demandes_terminees = mes_demandes.filter(statut='terminée').count()
    
    # Demandes récentes
    demandes_recentes = mes_demandes.order_by('-datedemande')[:5]
    
    # Domaines disponibles
    domaines = Domaine.objects.all()
    
    # ⭐ AJOUT DE LA MÉTÉO ⭐
    ville = "Douala"  # Ville par défaut
    weather_data = get_weather_data(ville)
    
    context = {
        'client': client,
        'total_demandes': total_demandes,
        'demandes_en_attente': demandes_en_attente,
        'demandes_en_cours': demandes_en_cours,
        'demandes_terminees': demandes_terminees,
        'demandes_recentes': demandes_recentes,
        'domaines': domaines,
        'weather': weather_data,  # ⭐ Données météo ajoutées
    }
    
    return render(request, 'dashboard/client_dashboard.html', context)
# Ajoutez ces imports en haut de views.py
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
import secrets

# Ajoutez ces fonctions dans views.py

def password_reset_request(request):
    """
    Demande de réinitialisation de mot de passe.
    L'utilisateur entre son email.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        
        try:
            # Utiliser .first() pour gérer les doublons
            utilisateur = Utilisateur.objects.filter(email=email).first()
            
            if utilisateur:
                # Générer un token de réinitialisation
                token = secrets.token_urlsafe(32)
                
                # Stocker le token dans la session (expire après 1h)
                request.session[f'reset_token_{utilisateur.id}'] = token
                request.session.set_expiry(3600)  # 1 heure
                
                # Créer le lien de réinitialisation
                uid = urlsafe_base64_encode(force_bytes(utilisateur.id))
                reset_link = request.build_absolute_uri(
                    f'/password-reset-confirm/{uid}/{token}/'
                )
                
                # Stocker le lien dans la session pour l'afficher
                request.session['reset_link'] = reset_link
                request.session['reset_email'] = email
                
                messages.success(request, 'Lien de réinitialisation généré avec succès !')
                return redirect('password_reset_request')
            else:
                # Pour des raisons de sécurité, on ne dit pas que l'email n'existe pas
                messages.info(request, 'Si cet email existe, un lien de réinitialisation sera généré.')
            
            return redirect('password_reset_request')
            
        except Exception as e:
            messages.error(request, f'Une erreur est survenue : {str(e)}')
            return redirect('password_reset_request')
    
    # Récupérer le lien s'il existe
    reset_link = request.session.get('reset_link')
    reset_email = request.session.get('reset_email')
    
    # Nettoyer la session après affichage
    if reset_link:
        request.session.pop('reset_link', None)
        request.session.pop('reset_email', None)
    
    return render(request, 'accounts/password_reset_request.html', {
        'reset_link': reset_link,
        'reset_email': reset_email
    })

def password_reset_confirm(request, uidb64, token):
    """
    Confirmation et nouveau mot de passe.
    """
    try:
        # Décoder l'ID utilisateur
        uid = force_str(urlsafe_base64_decode(uidb64))
        utilisateur = Utilisateur.objects.get(id=uid)
        
        # Vérifier le token
        stored_token = request.session.get(f'reset_token_{utilisateur.id}')
        
        if not stored_token or stored_token != token:
            messages.error(request, 'Le lien de réinitialisation est invalide ou a expiré.')
            return redirect('login')
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')
            
            # Validation
            if not new_password or len(new_password) < 6:
                messages.error(request, 'Le mot de passe doit contenir au moins 6 caractères.')
                return render(request, 'accounts/password_reset_confirm.html', {
                    'uidb64': uidb64,
                    'token': token
                })
            
            if new_password != confirm_password:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
                return render(request, 'accounts/password_reset_confirm.html', {
                    'uidb64': uidb64,
                    'token': token
                })
            
            # Mettre à jour le mot de passe
            utilisateur.password = make_password(new_password)
            utilisateur.save()
            
            # Supprimer le token de la session
            if f'reset_token_{utilisateur.id}' in request.session:
                del request.session[f'reset_token_{utilisateur.id}']
            
            messages.success(request, 'Votre mot de passe a été réinitialisé avec succès !')
            return redirect('login')
        
        return render(request, 'accounts/password_reset_confirm.html', {
            'uidb64': uidb64,
            'token': token,
            'utilisateur': utilisateur
        })
        
    except (TypeError, ValueError, OverflowError, Utilisateur.DoesNotExist):
        messages.error(request, 'Le lien de réinitialisation est invalide.')
        return redirect('login')
# ==================== FONCTION UTILITAIRE MÉTÉO ====================

