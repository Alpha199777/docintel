# 📄 DocIntel

Extraction intelligente de données depuis des PDFs bancaires via LLM.

Projet conçu pour s'intégrer dans les entreprises bancaires.

---

## Lancer en une commande
```bash
cp backend/.env.example backend/.env
# Remplir OPENAI_API_KEY dans backend/.env
docker compose up
```

- Frontend : http://localhost:3000
- API Swagger : http://localhost:8000/docs
> ⚠️ Ces liens fonctionnent uniquement après avoir lancé le projet en local.
---

## 🏗️ Architecture
```
[PDF] → FastAPI (extraction) → GPT-4o (structuration) → JSON
                                     ↑
                              React UI (upload + affichage)
```

---

## 📦 Stack

| Couche | Technologie |
|---|---|
| API | Python 3.11, FastAPI |
| Extraction PDF | pdfplumber, pymupdf |
| LLM | OpenAI GPT-4o |
| Frontend | React + Vite |
| Déploiement | Docker, Docker Compose |
| Tests | pytest |

---

## 🔌 Endpoints

| Méthode | Route | Description |
|---|---|---|
| GET | `/health` | Santé du service |
| POST | `/api/v1/extract` | Extraction texte brut |
| POST | `/api/v1/analyze` | PDF → JSON structuré via LLM |
| POST | `/api/v1/benchmark` | Comparaison des extracteurs |

---

## 📊 Évaluation des approches

| Extracteur | Vitesse | Tableaux | Usage recommandé |
|---|---|---|---|
| pdfplumber | ~500ms | ✅ Oui | Relevés bancaires |
| pymupdf | ~25ms | ❌ Non | Contrats, formulaires |

---

## 🔒 Sécurité

- Clé API dans `.env` — jamais dans le code
- Validation stricte du type de fichier (PDF uniquement)
- `temperature=0` — pas d'hallucination sur données financières

---

## 🗺️ Roadmap

- [ ] PostgreSQL — historique des extractions
- [ ] Ollama — mode on-prem sans API externe
- [ ] Fine-tuning — modèle spécialisé documents bancaires
- [ ] Auth — JWT pour sécuriser les endpoints
