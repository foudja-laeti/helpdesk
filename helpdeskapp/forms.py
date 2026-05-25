from django import forms
from .models import *
# make_password n'est plus nécessaire ici car la logique de hachage est dans la vue
# from django.contrib.auth.hashers import make_password 


class DomaineForm(forms.ModelForm):
    class Meta:
        model = Domaine
        fields =['intitule', 'description']
        widgets = {
            'intitule': forms.TextInput(attrs= {
                'class': 'input w-full',
                'placeholder': 'Entrez le domaine'
            }),
            'description': forms.Textarea(attrs= {
                'class': 'textarea w-full h-24',
                'placeholder': 'Decrire en quelques mots le domaine'

            })
        }


class UtilisateurForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'telephone', 'adresse', 'email', 'password', 'role']
        widgets = {
            'nom': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez le nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez le prénom'
            }),
            'telephone': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez le numéro de téléphone'
            }),
            'adresse': forms.Textarea(attrs={
                'class': 'textarea w-full h-24',
                'placeholder': 'Entrez l\'adresse'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez l\'email'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez le mot de passe'
            }),
            'role': forms.Select(attrs={
                'class': 'select w-full'
            })
        }
    
    # La méthode clean_password est retirée ici pour éviter le double hachage.
    # Le hachage est géré dans views.py lors de la sauvegarde.


class DemandeForm(forms.ModelForm):
    """
    Formulaire pour la création et la modification d'une Demande.
    """
    class Meta:
        model = Demande
        # ⭐ Ajout du champ 'adresse'
        fields = ['client', 'technicien', 'domaine', 'intitule', 'description', 'statut', 'adresse']
        
        widgets = {
            'client': forms.Select(attrs={
                'class': 'select w-full'
            }),
            'technicien': forms.Select(attrs={
                'class': 'select w-full'
            }),
            'domaine': forms.Select(attrs={
                'class': 'select w-full'
            }),
            'statut': forms.Select(attrs={
                'class': 'select w-full'
            }),
            'intitule': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Entrez le titre de la demande'
            }),
            'description': forms.Textarea(attrs={
                'class': 'textarea w-full h-24', 
                'placeholder': 'Décrivez la requête en détail'
            }),
            # ⭐ Widget pour le champ adresse
            'adresse': forms.TextInput(attrs={
                'class': 'input w-full',
                'placeholder': 'Ex: Douala, Akwa - Rue de la liberté'
            }),
        }

class LoginForm(forms.Form):
    """
    Formulaire simple pour la connexion (authentification).
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Votre email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'input w-full',
            'placeholder': 'Votre mot de passe'
        })
    )