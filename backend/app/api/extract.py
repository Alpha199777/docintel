# extract.py — Route HTTP pour l'extraction PDF
# But : recevoir un fichier PDF via HTTP, appeler le service,
# retourner le résultat. Cette couche ne contient PAS de logique métier.

import tempfile
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_extractor import (
    extract_with_pdfplumber,
    extract_with_pymupdf
)

router = APIRouter(prefix="/api/v1")


@router.post("/extract")
async def extract_pdf(
    file: UploadFile = File(...),
    extractor: str = "pdfplumber"  # paramètre optionnel : "pdfplumber" ou "pymupdf"
):
    """
    Extrait le texte d'un PDF uploadé.
    - **file** : le fichier PDF
    - **extractor** : "pdfplumber" (défaut) ou "pymupdf"
    """
    # Vérification de sécurité : on n'accepte que les PDFs
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés")

    # On sauvegarde temporairement le fichier uploadé sur le disque
    # tempfile le supprime automatiquement après usage
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    # On mesure le temps d'extraction (début de nos métriques)
    start = time.time()

    try:
        if extractor == "pymupdf":
            result = extract_with_pymupdf(tmp_path)
        else:
            result = extract_with_pdfplumber(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur d'extraction : {str(e)}")

    result["duration_ms"] = round((time.time() - start) * 1000, 2)
    result["filename"] = file.filename

    return result