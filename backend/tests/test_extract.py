# test_extract.py — Teste le endpoint d'extraction
# On crée un mini PDF en mémoire pour ne pas dépendre d'un fichier externe

import io
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_extract_rejects_non_pdf():
    """Un fichier non-PDF doit retourner une erreur 400."""
    fake_file = io.BytesIO(b"ceci n'est pas un pdf")
    response = client.post(
        "/api/v1/extract",
        files={"file": ("document.txt", fake_file, "text/plain")}
    )
    assert response.status_code == 400


def test_extract_accepts_pdf():
    """Un PDF valide doit retourner un résultat avec les bonnes clés."""
    # PDF minimal valide (structure PDF de base)
    minimal_pdf = b"%PDF-1.4\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 612 792]>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n190\n%%EOF"
    pdf_file = io.BytesIO(minimal_pdf)
    response = client.post(
        "/api/v1/extract",
        files={"file": ("test.pdf", pdf_file, "application/pdf")}
    )
    assert response.status_code == 200
    data = response.json()
    assert "text" in data
    assert "extractor" in data
    assert "duration_ms" in data