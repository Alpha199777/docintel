# evaluator.py — Service d'évaluation et comparaison d'approches
# But : mesurer objectivement chaque extracteur sur les mêmes données
# C'est la base d'une recommandation technique argumentée

import time
from app.services.pdf_extractor import (
    extract_with_pdfplumber,
    extract_with_pymupdf
)


def benchmark_extractors(pdf_path: str) -> dict:
    """
    Teste les deux extracteurs sur le même PDF.
    Retourne un rapport comparatif avec métriques objectives.
    """
    results = {}

    # --- Extracteur A : pdfplumber ---
    start = time.time()
    try:
        result_a = extract_with_pdfplumber(pdf_path)
        results["pdfplumber"] = {
            "status": "ok",
            "duration_ms": round((time.time() - start) * 1000, 2),
            "pages": result_a["pages"],
            "text_length": len(result_a["text"]),
            "tables_found": result_a["tables_found"],
            "text_preview": result_a["text"][:300]
        }
    except Exception as e:
        results["pdfplumber"] = {"status": "error", "detail": str(e)}

    # --- Extracteur B : pymupdf ---
    start = time.time()
    try:
        result_b = extract_with_pymupdf(pdf_path)
        results["pymupdf"] = {
            "status": "ok",
            "duration_ms": round((time.time() - start) * 1000, 2),
            "pages": result_b["pages"],
            "text_length": len(result_b["text"]),
            "tables_found": result_b["tables_found"],
            "text_preview": result_b["text"][:300]
        }
    except Exception as e:
        results["pymupdf"] = {"status": "error", "detail": str(e)}

    # --- Recommandation automatique ---
    recommendation = _recommend(results)

    return {
        "extractors": results,
        "recommendation": recommendation
    }


def _recommend(results: dict) -> dict:
    """
    Produit une recommandation automatique basée sur les métriques.
    Logique : on favorise la détection de tableaux pour docs bancaires,
    puis la vitesse comme critère secondaire.
    """
    a = results.get("pdfplumber", {})
    b = results.get("pymupdf", {})

    # Si l'un des deux a échoué
    if a.get("status") == "error":
        return {"winner": "pymupdf", "reason": "pdfplumber en erreur"}
    if b.get("status") == "error":
        return {"winner": "pdfplumber", "reason": "pymupdf en erreur"}

    # Critère 1 : tableaux détectés (priorité pour docs bancaires)
    if a["tables_found"] > b["tables_found"]:
        return {
            "winner": "pdfplumber",
            "reason": f"Détecte {a['tables_found']} tableau(x) vs 0 pour pymupdf",
            "use_case": "Documents avec tableaux (relevés, rapports)"
        }

    # Critère 2 : vitesse (si pas de tableaux)
    if b["duration_ms"] < a["duration_ms"]:
        return {
            "winner": "pymupdf",
            "reason": f"Plus rapide ({b['duration_ms']}ms vs {a['duration_ms']}ms)",
            "use_case": "Documents textuels (contrats, formulaires)"
        }

    return {
        "winner": "pdfplumber",
        "reason": "Défaut — meilleure précision générale",
        "use_case": "Usage général"
    }