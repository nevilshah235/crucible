"use client"

import { useCallback, useEffect, useState } from "react"
import Link from "next/link"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

type Source = { doc_id: string; name: string; type: string; created_at: string | null }
type Draft = { id: string; type: string; payload: Record<string, unknown>; updated_at: string | null }

export default function AdminPage() {
  const [sources, setSources] = useState<Source[]>([])
  const [drafts, setDrafts] = useState<Draft[]>([])
  const [selectedDraftIds, setSelectedDraftIds] = useState<Set<string>>(new Set())

  const [pdfFile, setPdfFile] = useState<File | null>(null)
  const [urlsText, setUrlsText] = useState("")
  const [topic, setTopic] = useState("system design fundamentals")

  const [loading, setLoading] = useState<string | null>(null)
  const [message, setMessage] = useState<{ type: "ok" | "err"; text: string } | null>(null)

  const fetchSources = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/admin/ingest/sources`)
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setSources(data.sources || [])
    } catch (e) {
      setMessage({ type: "err", text: String(e) })
    }
  }, [])

  const fetchDrafts = useCallback(async () => {
    try {
      const res = await fetch(`${API_URL}/admin/curriculum/drafts`)
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setDrafts(data.drafts || [])
    } catch (e) {
      setMessage({ type: "err", text: String(e) })
    }
  }, [])

  useEffect(() => {
    fetchSources()
    fetchDrafts()
  }, [fetchSources, fetchDrafts])

  const handleUploadPdf = async () => {
    if (!pdfFile) {
      setMessage({ type: "err", text: "Select a PDF file" })
      return
    }
    setLoading("pdf")
    setMessage(null)
    try {
      const form = new FormData()
      form.append("file", pdfFile)
      const res = await fetch(`${API_URL}/admin/ingest/pdf`, { method: "POST", body: form })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setMessage({ type: "ok", text: `Ingested: ${data.name}` })
      setPdfFile(null)
      fetchSources()
    } catch (e) {
      setMessage({ type: "err", text: String(e) })
    } finally {
      setLoading(null)
    }
  }

  const handleIngestUrls = async () => {
    const urls = urlsText.trim().split(/\n/).map((u) => u.trim()).filter(Boolean)
    if (!urls.length) {
      setMessage({ type: "err", text: "Enter at least one URL" })
      return
    }
    setLoading("urls")
    setMessage(null)
    try {
      const res = await fetch(`${API_URL}/admin/ingest/urls`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ urls }),
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      const count = (data.results || []).filter((r: { doc_id?: string }) => r.doc_id).length
      setMessage({ type: "ok", text: `Ingested ${count} URL(s)` })
      setUrlsText("")
      fetchSources()
    } catch (e) {
      setMessage({ type: "err", text: String(e) })
    } finally {
      setLoading(null)
    }
  }

  const handleGenerate = async () => {
    setLoading("generate")
    setMessage(null)
    try {
      const res = await fetch(`${API_URL}/admin/curriculum/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ topic: topic || "system design fundamentals" }),
      })
      if (!res.ok) throw new Error(await res.text())
      const data = await res.json()
      setMessage({ type: "ok", text: `Created ${(data.draft_ids || []).length} draft(s)` })
      fetchDrafts()
    } catch (e) {
      setMessage({ type: "err", text: String(e) })
    } finally {
      setLoading(null)
    }
  }

  const handlePublish = async () => {
    const ids = Array.from(selectedDraftIds)
    if (!ids.length) {
      setMessage({ type: "err", text: "Select at least one draft" })
      return
    }
    setLoading("publish")
    setMessage(null)
    try {
      const res = await fetch(`${API_URL}/admin/curriculum/publish`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ draft_ids: ids }),
      })
      if (!res.ok) throw new Error(await res.text())
      setMessage({ type: "ok", text: `Published ${ids.length} draft(s)` })
      setSelectedDraftIds(new Set())
      fetchDrafts()
    } catch (e) {
      setMessage({ type: "err", text: String(e) })
    } finally {
      setLoading(null)
    }
  }

  const toggleDraft = (id: string) => {
    setSelectedDraftIds((prev) => {
      const next = new Set(prev)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const selectAllDrafts = () => {
    setSelectedDraftIds(new Set(drafts.map((d) => d.id)))
  }

  const draftSummary = (d: Draft) => {
    const p = d.payload as Record<string, unknown>
    if (d.type === "concept") return (p.title as string) || d.id
    if (d.type === "quiz") return `Quiz for ${p.conceptId ?? p.concept_id ?? "?"}`
    if (d.type === "failure") return (p.fact as string)?.slice(0, 50) || d.id
    return d.id
  }

  return (
    <main>
      <p style={{ marginBottom: "1rem" }}>
        <Link href="/">← Learner app</Link>
      </p>
      <h1>Admin</h1>
      {message && (
        <p
          style={{
            padding: "0.5rem",
            background: message.type === "err" ? "#fee" : "#efe",
            marginBottom: "1rem",
          }}
        >
          {message.text}
        </p>
      )}

      <section>
        <h2>Sources (ingest into LightRAG)</h2>
        <p style={{ fontSize: "0.9rem", color: "#555" }}>
          Upload a PDF or submit URLs; content is extracted and inserted into LightRAG (Gemini). Then generate curriculum below.
        </p>
        <div style={{ marginBottom: "0.75rem" }}>
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setPdfFile(e.target.files?.[0] ?? null)}
          />
          <button
            type="button"
            onClick={handleUploadPdf}
            disabled={loading === "pdf" || !pdfFile}
            style={{ marginLeft: "0.5rem" }}
          >
            {loading === "pdf" ? "Uploading…" : "Upload PDF"}
          </button>
        </div>
        <div style={{ marginBottom: "0.75rem" }}>
          <textarea
            placeholder="One URL per line"
            value={urlsText}
            onChange={(e) => setUrlsText(e.target.value)}
            rows={3}
            style={{ width: "100%", maxWidth: "480px", display: "block", marginBottom: "0.25rem" }}
          />
          <button
            type="button"
            onClick={handleIngestUrls}
            disabled={loading === "urls"}
          >
            {loading === "urls" ? "Ingesting…" : "Ingest URLs"}
          </button>
        </div>
        <div>
          <button type="button" onClick={fetchSources} style={{ marginBottom: "0.5rem" }}>
            Refresh sources
          </button>
          <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
            {sources.length === 0 && <li style={{ color: "#888" }}>No ingested sources yet.</li>}
            {sources.map((s) => (
              <li key={s.doc_id} style={{ marginBottom: "0.25rem" }}>
                <span style={{ fontWeight: 600 }}>{s.type}</span> — {s.name}
                {s.created_at && <span style={{ color: "#666", marginLeft: "0.5rem" }}>{s.created_at.slice(0, 10)}</span>}
              </li>
            ))}
          </ul>
        </div>
      </section>

      <section>
        <h2>Generate curriculum</h2>
        <p style={{ fontSize: "0.9rem", color: "#555" }}>
          Query LightRAG by topic and synthesize concepts, quizzes, and failure facts with Gemini. Results are saved as drafts.
        </p>
        <div style={{ display: "flex", gap: "0.5rem", alignItems: "center", flexWrap: "wrap", marginBottom: "0.5rem" }}>
          <label>
            Topic:{" "}
            <input
              type="text"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              style={{ width: "220px", padding: "0.35rem" }}
            />
          </label>
          <button
            type="button"
            onClick={handleGenerate}
            disabled={loading === "generate"}
          >
            {loading === "generate" ? "Generating…" : "Generate curriculum"}
          </button>
        </div>
      </section>

      <section>
        <h2>Drafts</h2>
        <p style={{ fontSize: "0.9rem", color: "#555" }}>
          Select drafts to publish to the learner app (concepts, quizzes, failure_facts in DB).
        </p>
        <div style={{ marginBottom: "0.5rem" }}>
          <button type="button" onClick={fetchDrafts}>
            Refresh drafts
          </button>
          <button type="button" onClick={selectAllDrafts} style={{ marginLeft: "0.5rem" }}>
            Select all
          </button>
        </div>
        <ul style={{ listStyle: "none", padding: 0, margin: 0 }}>
          {drafts.length === 0 && <li style={{ color: "#888" }}>No drafts yet. Generate curriculum first.</li>}
          {drafts.map((d) => (
            <li key={d.id} style={{ marginBottom: "0.35rem", display: "flex", alignItems: "flex-start", gap: "0.5rem" }}>
              <input
                type="checkbox"
                checked={selectedDraftIds.has(d.id)}
                onChange={() => toggleDraft(d.id)}
              />
              <span>
                <span style={{ fontWeight: 600 }}>{d.type}</span> — {draftSummary(d)}
              </span>
            </li>
          ))}
        </ul>
        <div style={{ marginTop: "0.75rem" }}>
          <button
            type="button"
            onClick={handlePublish}
            disabled={loading === "publish" || selectedDraftIds.size === 0}
          >
            {loading === "publish" ? "Publishing…" : `Publish selected (${selectedDraftIds.size})`}
          </button>
        </div>
      </section>
    </main>
  )
}
