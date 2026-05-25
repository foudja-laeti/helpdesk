# 📋 Guide de Contribution — Projet Helpdesk

Bienvenue sur le projet **Helpdesk** ! Ce document définit les règles et conventions
à respecter pour contribuer au projet de manière cohérente et professionnelle.

---

## 🌿 Stratégie de Branches (Gitflow)

Nous utilisons une stratégie **Gitflow** adaptée à une équipe de 3 développeurs.

```
main
 └── develop
      ├── feature/api-delivery
      ├── feature/<nom-de-la-fonctionnalité>
      └── hotfix/<nom-du-correctif>
```

### Description des branches

| Branche | Rôle | Protection |
|---|---|---|
| `main` | Code stable en production | ✅ Protégée — PR obligatoire |
| `develop` | Intégration des nouvelles fonctionnalités | ✅ PR recommandée |
| `feature/*` | Développement d'une fonctionnalité | ❌ Libre |
| `hotfix/*` | Correctif urgent en production | PR vers `main` + `develop` |

### Règles de protection sur `main`

- ❌ **Force push interdit**
- ✅ **Pull Request obligatoire** avant tout merge
- ✅ **Revue par au moins 1 pair** requise avant validation
- ✅ **Tous les tests CI doivent passer** avant le merge

---

## 🔀 Workflow de développement

```bash
# 1. Toujours partir de develop à jour
git checkout develop
git pull origin develop

# 2. Créer une branche de fonctionnalité
git checkout -b feature/nom-de-la-fonctionnalite

# 3. Travailler, committer régulièrement
git add .
git commit -m "feat(module): description courte de la modification"

# 4. Pousser la branche
git push origin feature/nom-de-la-fonctionnalite

# 5. Ouvrir une Pull Request vers develop sur GitHub/GitLab
# 6. Après revue et approbation → merge via l'interface
```

---

## ✍️ Convention de Commits (Conventional Commits)

Tous les messages de commit **doivent** suivre la convention
[Conventional Commits](https://www.conventionalcommits.org/fr/).

### Format

```
<type>(<scope>): <description courte>

[corps optionnel]

[pied de page optionnel]
```

### Types autorisés

| Type | Usage |
|---|---|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `docs` | Modification de documentation uniquement |
| `style` | Formatage, espaces, virgules (sans changement de logique) |
| `refactor` | Refactorisation du code (ni feat, ni fix) |
| `test` | Ajout ou modification de tests |
| `chore` | Tâches de maintenance (dépendances, config CI...) |
| `ci` | Modification des fichiers CI/CD |
| `perf` | Amélioration des performances |
| `revert` | Annulation d'un commit précédent |

### Scopes recommandés pour ce projet

| Scope | Module concerné |
|---|---|
| `auth` | Authentification (login, logout, register) |
| `demande` | Gestion des demandes |
| `utilisateur` | Gestion des utilisateurs |
| `domaine` | Gestion des domaines |
| `dashboard` | Tableaux de bord |
| `ci` | Pipeline CI/CD |
| `docker` | Dockerfile et configuration Docker |
| `tests` | Fichiers de tests |
| `settings` | Configuration Django |

### Exemples de commits valides ✅

```bash
feat(auth): ajouter la réinitialisation du mot de passe par email
fix(demande): corriger la redirection après suppression d'une demande
test(utilisateur): ajouter les tests unitaires du CRUD utilisateur
ci(pipeline): configurer le stage SonarQube dans GitHub Actions
docs: mettre à jour le README avec les instructions d'installation
chore(docker): optimiser le Dockerfile avec un build multi-stage
refactor(views): extraire la logique météo dans un service dédié
```

### Exemples de commits invalides ❌

```bash
# Trop vague
git commit -m "fix bug"
git commit -m "update"
git commit -m "wip"

# Pas de type
git commit -m "correction de la page login"

# Message en majuscules sans type
git commit -m "AJOUT FONCTIONNALITÉ"
```

---

## 🔍 Revue de Code (Code Review)

### Avant d'ouvrir une Pull Request

- [ ] Les tests passent localement (`python manage.py test`)
- [ ] La couverture de tests est ≥ 80%
- [ ] Aucune clé API ou secret dans le code
- [ ] Le code respecte les conventions PEP8
- [ ] La description de la PR est claire et complète

### Critères de revue

Le relecteur vérifie :
- La logique métier est correcte
- Pas de régression sur les fonctionnalités existantes
- Le code est lisible et commenté si nécessaire
- Les tests couvrent les cas nominaux et les cas d'erreur

---

## 🛠️ Installation locale

```bash
# Cloner le dépôt
git clone https://github.com/<organisation>/helpdesk.git
cd helpdesk

# Créer l'environnement virtuel
python -m venv env
source env/bin/activate  # Linux/macOS
# ou
env\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt

# Appliquer les migrations
python manage.py migrate

# Lancer le serveur de développement
python manage.py runserver
```

---

## 🧪 Lancer les tests

```bash
# Lancer tous les tests
python manage.py test

# Avec rapport de couverture
pip install coverage
coverage run manage.py test
coverage report
coverage html  # Rapport HTML dans htmlcov/
```

---

## 📁 Structure du projet

```
helpdesk/
├── helpdesk_project/        # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── helpdeskapp/             # Application principale
│   ├── models.py            # Modèles : Utilisateur, Domaine, Demande
│   ├── views.py             # Vues et logique métier
│   ├── forms.py             # Formulaires
│   ├── urls.py              # Routes de l'application
│   ├── middleware.py        # Middleware d'authentification
│   ├── templates/           # Templates HTML
│   └── tests/               # Tests unitaires
├── logs/                    # Fichiers de logs (ignorés par Git)
├── .github/workflows/       # Pipeline CI/CD GitHub Actions
├── Dockerfile               # Image Docker de l'application
├── docker-compose.yml       # Orchestration locale
├── requirements.txt         # Dépendances Python
├── sonar-project.properties # Configuration SonarQube
├── .gitignore
└── CONTRIBUTING.md          # Ce fichier
```

---

## 🔐 Sécurité

- **Ne jamais committer** de clés API, mots de passe ou tokens dans le code
- Utiliser les **variables d'environnement** ou les **secrets GitHub/GitLab**
- Le fichier `.env` est dans le `.gitignore`
- En cas de commit accidentel d'un secret → alerter immédiatement l'équipe et révoquer la clé

---

## 📞 Contact

Pour toute question sur le projet, ouvrir une **Issue** sur le dépôt avec le label approprié (`bug`, `question`, `enhancement`).