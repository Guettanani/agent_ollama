#!/bin/bash

# Création des volumes s'ils n'existent pas
if ! docker volume ls | grep -q ollama_data; then
    echo "Création du volume ollama_data..."
    docker volume create ollama_data
fi

if ! docker volume ls | grep -q openwebui_data; then
    echo "Création du volume openwebui_data..."
    docker volume create openwebui_data
fi

# Démarrage des containers
echo "Démarrage des services..."
docker compose up -d

# Vérification du statut
echo "Statut des containers :"
docker compose ps