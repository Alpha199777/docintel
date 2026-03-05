# Dockerfile backend — Image Python pour l'API FastAPI
# On part d'une image officielle Python légère (slim = sans superflu)
FROM python:3.11-slim

# Répertoire de travail dans le conteneur
WORKDIR /app

# On copie d'abord les dépendances AVANT le code
# Pourquoi ? Docker met en cache chaque étape — si requirements.txt
# ne change pas, il ne réinstalle pas tout à chaque build
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ensuite on copie le code
COPY app/ ./app/

# Port exposé par l'API
EXPOSE 8000

# Commande de démarrage
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]