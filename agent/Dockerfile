# FROM python:3.9-slim

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY agent.py .

# CMD ["python", "agent.py"]


# FROM python:3.9-slim

# WORKDIR /app

# # Installation des dépendances
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# # Configuration de l'environnement pour gérer correctement les signaux
# ENV PYTHONUNBUFFERED=1

# # Copie du code
# COPY agent.py .

# # Commande de démarrage
# CMD ["python", "-u", "agent.py"]



FROM python:3.9-slim

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Configuration de l'environnement
ENV PYTHONUNBUFFERED=1

# Copie du code
COPY *.py .

# Volume pour la persistance de la mémoire
VOLUME ["/app/data"]

# Commande de démarrage
CMD ["python", "-u", "agent.py"]