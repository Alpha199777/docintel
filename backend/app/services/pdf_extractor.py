# pdf_extractor.py — Service d'extraction de texte depuis un PDF
# But : contenir TOUTE la logique d'extraction, indépendamment de l'API
# Principe : un service ne sait pas qu'il y a une API au-dessus de lui

import pdfplumber
import fitz  # pymupdf
from pathlib import Path


def extract_with_pdfplumber(pdf_path: str) -> dict:
    """
    Approche A : pdfplumber
    Point fort : détecte et extrait les tableaux proprement
    """
    text_pages = []
    tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            # Extraire le texte brut de la page
            text = page.extract_text() or ""
            text_pages.append(text)

            # Extraire les tableaux si présents
            page_tables = page.extract_tables()
            if page_tables:
                tables.append({
                    "page": i + 1,
                    "tables": page_tables
                })

    return {
        "extractor": "pdfplumber",
        "pages": len(text_pages),
        "text": "\n\n--- PAGE SUIVANTE ---\n\n".join(text_pages),
        "tables_found": len(tables),
        "tables": tables
    }


def extract_with_pymupdf(pdf_path: str) -> dict:
    """
    Approche B : pymupdf (fitz)
    Point fort : rapide, robuste sur PDFs complexes/scannés
    """
    text_pages = []

    doc = fitz.open(pdf_path)
    for page in doc:
        text = page.get_text()
        text_pages.append(text)
    doc.close()

    return {
        "extractor": "pymupdf",
        "pages": len(text_pages),
        "text": "\n\n--- PAGE SUIVANTE ---\n\n".join(text_pages),
        "tables_found": 0,  # pymupdf ne détecte pas les tableaux nativement
        "tables": []
    }