# analyze.py — Route HTTP du pipeline complet
# But : orchestrer les deux services qu'on a créés
# Étape 1 : extraction texte brut (Sprint 2)
# Étape 2 : structuration via LLM (Sprint 3)
# Cette route ne contient pas de logique métier — elle coordonne

import tempfile
import time
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.pdf_extractor import extract_with_pdfplumber
from app.services.llm_extractor import extract_structured_data

router = APIRouter(prefix="/api/v1")


@router.post("/analyze")
async def analyze_pdf(file: UploadFile = File(...)):
    """
    Pipeline complet : PDF → texte brut → JSON structuré via GPT-4o.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les PDFs sont acceptés")

    # Sauvegarde temporaire du fichier uploadé
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    total_start = time.time()

    # Étape 1 : PDF → texte brut
    try:
        pdf_result = extract_with_pdfplumber(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur extraction PDF : {e}")

    # Étape 2 : texte brut → JSON structuré
    try:
        llm_result = extract_structured_data(pdf_result["text"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur LLM : {e}")

    return {
        "filename": file.filename,
        "extracted_data": llm_result["extracted"],
        "metrics": {
            "total_duration_ms": round((time.time() - total_start) * 1000, 2),
            "pages": pdf_result["pages"],
            "tokens_used": llm_result["tokens_used"],
            "model": llm_result["model"]
        }
    }