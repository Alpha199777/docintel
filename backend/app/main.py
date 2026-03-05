# main.py — Point d'entrée FastAPI
# On branche ici toutes les routes de l'application
# Chaque nouveau module API s'ajoute avec include_router

from fastapi import FastAPI
from app.api import health, extract, analyze

app = FastAPI(
    title="DocIntel API",
    description="Extraction intelligente de données depuis des PDFs bancaires",
    version="0.3.0",
)

app.include_router(health.router)
app.include_router(extract.router)
app.include_router(analyze.router)