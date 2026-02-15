"use client"

import { useCallback, useEffect, useState } from "react"
import { ConceptView } from "@/components/ConceptView"
import { CoachReply } from "@/components/CoachReply"
import { DesignForm } from "@/components/DesignForm"
import { PressureBlock } from "@/components/PressureBlock"
import { Quiz } from "@/components/Quiz"
import { apiFetch } from "@/lib/api"

type Concept = { id: string; title: string; body: string; tags?: string[] }
type QuizData = {
  id: string
  conceptId: string
  questions: { id: string; text: string; options: { id: string; text: string; correct: boolean }[] }[]
}

export default function Home() {
  const [concept, setConcept] = useState<Concept | null>(null)
  const [quiz, setQuiz] = useState<QuizData | null>(null)
  const [quizResult, setQuizResult] = useState<{ score: number; total: number; results: { questionId: string; correct: boolean }[] } | null>(null)
  const [designText, setDesignText] = useState("")
  const [coachFeedback, setCoachFeedback] = useState("")
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    Promise.all([
      apiFetch("/content/concept").then((r) => r.json()),
      apiFetch("/content/quiz").then((r) => r.json()),
    ])
      .then(([c, q]) => {
        setConcept(c)
        setQuiz(q)
      })
      .catch((e) => setError(String(e)))
      .finally(() => setLoading(false))
  }, [])

  const handleQuizSubmit = useCallback(
    async (answers: { questionId: string; selectedOptionId: string }[]) => {
      const res = await apiFetch("/quiz/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ answers }),
      })
      const data = await res.json()
      setQuizResult(data)
    },
    []
  )

  const handleDesignSubmit = useCallback(async (text: string) => {
    setDesignText(text)
    await apiFetch("/design/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ designText: text }),
    })
  }, [])

  const handleCoachFeedback = useCallback(
    async (pressureTest = false) => {
      const res = await apiFetch("/coach/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          designText: designText || "(no design submitted yet)",
          topic: "caching",
          pressureTest,
          conversationContext: [],
        }),
      })
      const data = await res.json()
      setCoachFeedback(data.feedback || "")
    },
    [designText]
  )

  const handlePressureTest = useCallback(() => {
    handleCoachFeedback(true)
  }, [handleCoachFeedback])

  if (loading) return <p>Loading...</p>
  if (error) return <p>Error: {error}. Is the backend running?</p>
  if (!concept || !quiz) return <p>Missing content.</p>

  return (
    <main>
      <h1>Crucible</h1>
      <ConceptView concept={concept} />
      <Quiz quiz={quiz} onSubmit={handleQuizSubmit} />
      {quizResult != null && (
        <p>
          Quiz: {quizResult.score} / {quizResult.total} correct.
        </p>
      )}
      <DesignForm onSubmit={handleDesignSubmit} />
      <section>
        <h2>Coach</h2>
        <button type="button" onClick={() => handleCoachFeedback(false)}>
          Get coach feedback
        </button>
        {coachFeedback ? <CoachReply feedback={coachFeedback} /> : null}
      </section>
      <PressureBlock onRequestPressure={handlePressureTest} />
    </main>
  )
}
