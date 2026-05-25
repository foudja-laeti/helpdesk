# ==================== STAGE 1 : BUILD ====================
FROM python:3.13-slim AS builder

WORKDIR /app

# Installer les dépendances système nécessaires
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copier et installer les dépendances Python
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements.txt


# ==================== STAGE 2 : PRODUCTION ====================
FROM python:3.13-slim AS production

WORKDIR /app

# Copier les dépendances installées depuis le stage builder
COPY --from=builder /install /usr/local

# Copier le code source
COPY . .

# ⭐ Sécurité : créer un utilisateur non-root
RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup --no-create-home appuser && \
    chown -R appuser:appgroup /app

# Basculer vers l'utilisateur non-root
USER appuser

# Variables d'environnement
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=helpdesk_project.settings

# Exposer le port
EXPOSE 8000

# Commande de démarrage
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
