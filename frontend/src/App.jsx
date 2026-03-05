// App.jsx — Interface principale de DocIntel
// But : uploader un PDF, appeler l'API, afficher le résultat
// On utilise useState pour gérer l'état de l'application

import { useState } from "react"

const API_URL = "http://127.0.0.1:8000/api/v1"

export default function App() {
  const [file, setFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [mode, setMode] = useState("analyze") // "analyze" ou "benchmark"

  async function handleSubmit() {
    if (!file) return
    setLoading(true)
    setError(null)
    setResult(null)

    // On construit la requête multipart/form-data
    // C'est le format standard pour envoyer des fichiers via HTTP
    const formData = new FormData()
    formData.append("file", file)

    try {
      const response = await fetch(`${API_URL}/${mode}`, {
        method: "POST",
        body: formData,
      })
      if (!response.ok) {
        const err = await response.json()
        throw new Error(err.detail || "Erreur API")
      }
      const data = await response.json()
      setResult(data)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={styles.container}>

      {/* En-tête */}
      <div style={styles.header}>
        <h1 style={styles.title}>📄 DocIntel</h1>
        <p style={styles.subtitle}>
          Extraction intelligente de données depuis des PDFs bancaires
        </p>
      </div>

      {/* Sélecteur de mode */}
      <div style={styles.modeSelector}>
        <button
          style={mode === "analyze" ? styles.btnActive : styles.btn}
          onClick={() => setMode("analyze")}
        >
          🔍 Analyser
        </button>
        <button
          style={mode === "benchmark" ? styles.btnActive : styles.btn}
          onClick={() => setMode("benchmark")}
        >
          📊 Benchmark
        </button>
      </div>

      {/* Zone d'upload */}
      <div style={styles.uploadZone}>
        <input
          type="file"
          accept=".pdf"
          onChange={(e) => setFile(e.target.files[0])}
          style={styles.fileInput}
        />
        {file && (
          <p style={styles.fileName}>✅ {file.name}</p>
        )}
        <button
          onClick={handleSubmit}
          disabled={!file || loading}
          style={file && !loading ? styles.btnPrimary : styles.btnDisabled}
        >
          {loading ? "⏳ Traitement en cours..." : "Lancer l'extraction"}
        </button>
      </div>

      {/* Erreur */}
      {error && (
        <div style={styles.error}>
          ❌ {error}
        </div>
      )}

      {/* Résultat */}
      {result && (
        <div style={styles.resultContainer}>

          {/* Métriques */}
          {result.metrics && (
            <div style={styles.metrics}>
              <h3>📊 Métriques</h3>
              <p>⏱ Durée : <strong>{result.metrics.total_duration_ms}ms</strong></p>
              <p>🔤 Tokens : <strong>{result.metrics.tokens_used}</strong></p>
              <p>🤖 Modèle : <strong>{result.metrics.model}</strong></p>
              <p>📄 Pages : <strong>{result.metrics.pages}</strong></p>
            </div>
          )}

          {/* Recommandation benchmark */}
          {result.recommendation && (
            <div style={styles.recommendation}>
              <h3>🏆 Recommandation</h3>
              <p>Vainqueur : <strong>{result.recommendation.winner}</strong></p>
              <p>Raison : {result.recommendation.reason}</p>
              <p>Usage : {result.recommendation.use_case}</p>
            </div>
          )}

          {/* JSON complet */}
          <div style={styles.jsonBlock}>
            <h3>📋 Résultat complet</h3>
            <pre style={styles.pre}>
              {JSON.stringify(result, null, 2)}
            </pre>
          </div>

        </div>
      )}
    </div>
  )
}

// Styles inline pour garder tout dans un seul fichier
const styles = {
  container: { maxWidth: 800, margin: "0 auto", padding: 32, fontFamily: "sans-serif", backgroundColor: "#f1f5f9", minHeight: "100vh" },
  header: { textAlign: "center", marginBottom: 32 },
  title: { fontSize: 32, margin: 0, color: "#0f172a" },
  subtitle: { color: "#475569", marginTop: 8 },
  modeSelector: { display: "flex", gap: 12, marginBottom: 24, justifyContent: "center" },
  btn: { padding: "8px 20px", borderRadius: 6, border: "1px solid #cbd5e1", cursor: "pointer", background: "#ffffff", color: "#0f172a" },
  btnActive: { padding: "8px 20px", borderRadius: 6, border: "2px solid #2563eb", cursor: "pointer", background: "#eff6ff", color: "#2563eb", fontWeight: "bold" },
  uploadZone: { border: "2px dashed #94a3b8", borderRadius: 12, padding: 32, textAlign: "center", marginBottom: 24, backgroundColor: "#ffffff" },
  fileInput: { marginBottom: 12, color: "#0f172a" },
  fileName: { color: "#16a34a", marginBottom: 12 },
  btnPrimary: { padding: "10px 28px", background: "#2563eb", color: "#ffffff", border: "none", borderRadius: 8, cursor: "pointer", fontSize: 16 },
  btnDisabled: { padding: "10px 28px", background: "#cbd5e1", color: "#ffffff", border: "none", borderRadius: 8, cursor: "not-allowed", fontSize: 16 },
  error: { background: "#fef2f2", border: "1px solid #fca5a5", borderRadius: 8, padding: 16, color: "#dc2626", marginBottom: 24 },
  resultContainer: { display: "flex", flexDirection: "column", gap: 16 },
  metrics: { background: "#f0fdf4", border: "1px solid #86efac", borderRadius: 8, padding: 16, color: "#14532d" },
  recommendation: { background: "#fefce8", border: "1px solid #fde047", borderRadius: 8, padding: 16, color: "#713f12" },
  jsonBlock: { background: "#ffffff", border: "1px solid #e2e8f0", borderRadius: 8, padding: 16, color: "#0f172a" },
  pre: { overflow: "auto", fontSize: 13, margin: 0, color: "#0f172a" }
}
