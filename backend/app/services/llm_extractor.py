# llm_extractor.py — Service d'extraction structurée via LLM
# But : prendre du texte brut et retourner un JSON métier propre
# Le prompt EST la logique métier — c'est le coeur du prompt engineering

import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# On instancie le client une seule fois (bonne pratique performance)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Le prompt système définit le "rôle" du LLM
# Plus ce rôle est précis, plus les extractions sont fiables
SYSTEM_PROMPT = """Tu es un assistant spécialisé dans l'extraction de données 
depuis des documents bancaires et financiers.

Ta mission : extraire les informations structurées du texte fourni et les retourner 
UNIQUEMENT en JSON valide, sans texte avant ni après.

Si une information est absente du document, utilise null.
Ne jamais inventer de données."""


def extract_structured_data(text: str) -> dict:
    """
    Appelle GPT-4o pour extraire les données structurées.
    Retourne un dict Python avec les données extraites.
    """
    if not text or len(text.strip()) < 10:
        raise ValueError("Texte trop court ou vide pour extraction")

    prompt = f"""Analyse ce document bancaire et extrais les informations en JSON :

{{
  "type_document": "type détecté (relevé, contrat, formulaire, autre)",
  "client": {{
    "nom": null,
    "prenom": null,
    "identifiant": null
  }},
  "institution": {{
    "nom": null,
    "iban": null,
    "bic": null
  }},
  "financier": {{
    "solde": null,
    "devise": null,
    "date_document": null
  }},
  "metadata": {{
    "langue": null,
    "confiance": "haute/moyenne/faible"
  }}
}}

TEXTE DU DOCUMENT :
---
{text[:4000]}
---

Retourne uniquement le JSON, rien d'autre."""

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        # temperature=0 : réponses déterministes, pas de créativité
        # Essentiel pour de l'extraction de données financières
        temperature=0,
        max_tokens=1000,
    )

    raw = response.choices[0].message.content.strip()

    try:
        return {
            "extracted": json.loads(raw),
            "model": "gpt-4o",
            "tokens_used": response.usage.total_tokens
        }
    except json.JSONDecodeError:
        # Si le LLM ajoute du texte autour du JSON, on l'isole
        start = raw.find("{")
        end = raw.rfind("}") + 1
        if start != -1 and end > start:
            return {
                "extracted": json.loads(raw[start:end]),
                "model": "gpt-4o",
                "tokens_used": response.usage.total_tokens
            }
        raise ValueError(f"Le LLM n'a pas retourné du JSON valide : {raw}")