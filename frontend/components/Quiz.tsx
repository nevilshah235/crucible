"use client"

import { useState } from "react"

type Option = { id: string; text: string; correct: boolean }
type Question = { id: string; text: string; options: Option[] }
type QuizData = { id: string; conceptId: string; questions: Question[] }

export function Quiz({
  quiz,
  onSubmit,
}: {
  quiz: QuizData
  onSubmit: (answers: { questionId: string; selectedOptionId: string }[]) => void
}) {
  const [selected, setSelected] = useState<Record<string, string>>({})

  const questions = quiz?.questions ?? []

  const handleSubmit = () => {
    const answers = questions.map((q) => ({
      questionId: q.id,
      selectedOptionId: selected[q.id] ?? "",
    }))
    onSubmit(answers)
  }

  return (
    <section>
      <h2>Quiz</h2>
      {questions.map((q) => (
        <div key={q.id} style={{ marginBottom: "1rem" }}>
          <p><strong>{q.text}</strong></p>
          {(q.options ?? []).map((opt) => (
            <label key={opt.id} style={{ display: "block", marginLeft: "1rem" }}>
              <input
                type="radio"
                name={q.id}
                value={opt.id}
                checked={selected[q.id] === opt.id}
                onChange={() => setSelected((s) => ({ ...s, [q.id]: opt.id }))}
              />
              {" "}{opt.text}
            </label>
          ))}
        </div>
      ))}
      <button type="button" onClick={handleSubmit}>
        Submit quiz
      </button>
    </section>
  )
}
