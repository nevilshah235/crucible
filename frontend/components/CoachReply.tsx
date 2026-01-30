"use client"

export function CoachReply({ feedback }: { feedback: string }) {
  return (
    <section>
      <h2>Coach</h2>
      <p style={{ whiteSpace: "pre-wrap" }}>{feedback}</p>
    </section>
  )
}
