"use client"

import { useState } from "react"

export function DesignForm({
  onSubmit,
}: {
  onSubmit: (designText: string) => void
}) {
  const [text, setText] = useState("")

  const handleSubmit = () => {
    onSubmit(text)
  }

  return (
    <section>
      <h2>Your design</h2>
      <p>Describe your system design in plain text.</p>
      <textarea
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="e.g. I'll use a cache in front of the DB..."
      />
      <br />
      <button type="button" onClick={handleSubmit}>
        Submit design
      </button>
    </section>
  )
}
