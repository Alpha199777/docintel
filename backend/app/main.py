from fastapi import FastAPI
from app.api import health

app = FastAPI(
    title="DocIntel API",
    description="Extraction intelligente de données depuis des PDFs bancaires",
    version="0.1.0",
)

app.include_router(health.router)
