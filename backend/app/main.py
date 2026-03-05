# main.py — Point d'entrée FastAPI
# On ajoute la nouvelle route extract au routeur principal

from fastapi import FastAPI
from app.api import health, extract

app = FastAPI(
    title="DocIntel API",
    description="Extraction intelligente de données depuis des PDFs bancaires",
    version="0.2.0",
)

app.include_router(health.router)
app.include_router(extract.router)