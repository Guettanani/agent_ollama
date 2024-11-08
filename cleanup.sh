#!/bin/bash

# Arrêt des containers
echo "Arrêt des services..."
docker compose down

# Option pour supprimer les volumes (décommenter si nécessaire)
# echo "Suppression des volumes..."
# docker volume rm ollama_data
# docker volume rm openwebui_datadi