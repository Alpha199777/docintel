# benchmark.py — Route HTTP pour la comparaison d'extracteurs
# But : exposer le service d'évaluation via un endpoint dédié
# Penses "mesure" et pas juste "ça marche"

import tempfile
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.evaluator import benchmark_extractors

router = APIRouter(prefix="/api/v1")


@router.post("/benchmark")
async def benchmark_pdf(file: UploadFile = File(...)):
    """
    Compare les deux extracteurs PDF sur le même fichier.
    Retourne métriques + recommandation automatique.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les PDFs sont acceptés")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        content = await file.read()
        tmp.write(content)
        tmp_path = tmp.name

    try:
        report = benchmark_extractors(tmp_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return report