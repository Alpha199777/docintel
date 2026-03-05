# main.py — Point d'entrée FastAPI
# On ajoute benchmark aux routes existantes

from fastapi import FastAPI
from app.api import health, extract, analyze, benchmark

app = FastAPI(
    title="DocIntel API",
    description="Extraction intelligente de données depuis des PDFs bancaires",
    version="0.4.0",
)

app.include_router(health.router)
app.include_router(extract.router)
app.include_router(analyze.router)
app.include_router(benchmark.router)