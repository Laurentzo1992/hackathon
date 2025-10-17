# Utiliser Python 3.11
FROM python:3.11-slim

# Variables d’environnement
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Répertoire de travail
WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Copier requirements.txt et installer
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code du projet
COPY . /app/

# Exposer le port Django
EXPOSE 8000

# Lancer Django avec Gunicorn
CMD ["gunicorn", "project.wsgi:application", "--bind", "0.0.0.0:8000"]
