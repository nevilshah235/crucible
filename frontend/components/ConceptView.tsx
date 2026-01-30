"use client"

type Concept = {
  id: string
  title: string
  body: string
  tags?: string[]
}

export function ConceptView({ concept }: { concept: Concept }) {
  return (
    <section>
      <h2>{concept.title}</h2>
      <p>{concept.body}</p>
      {concept.tags?.length ? (
        <p style={{ fontSize: "0.9rem", color: "#666" }}>
          Tags: {concept.tags.join(", ")}
        </p>
      ) : null}
    </section>
  )
}
