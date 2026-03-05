# main.py — On ajoute le middleware CORS
# Sans ça, le navigateur bloque toutes les requêtes du frontend vers l'API

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import health, extract, analyze, benchmark

app = FastAPI(
    title="DocIntel API",
    description="Extraction intelligente de données depuis des PDFs bancaires",
    version="0.4.0",
)

# On autorise le frontend React à appeler l'API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(extract.router)
app.include_router(analyze.router)
app.include_router(benchmark.router)