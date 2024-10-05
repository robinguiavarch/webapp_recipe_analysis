# Utiliser une image de base légère de Python 3.12
FROM python:3.12-slim

# Créer et définir le répertoire de travail pour l'application
WORKDIR /app

# Copier les fichiers de configuration de Poetry dans le conteneur
COPY pyproject.toml poetry.lock ./

# Installer Poetry dans le conteneur
RUN pip install poetry

# Installer les dépendances du projet à partir de Poetry
RUN poetry install

# Copier le reste des fichiers de l'application dans le conteneur
COPY . .

# Exposer le port que Streamlit utilise par défaut (8501)
EXPOSE 8501

# Commande pour démarrer l'application Streamlit
CMD ["poetry", "run", "streamlit", "run", "app/main.py"]
