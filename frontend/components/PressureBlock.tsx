"use client"

export function PressureBlock({
  onRequestPressure,
  disabled,
}: {
  onRequestPressure: () => void
  disabled?: boolean
}) {
  return (
    <section>
      <h2>Pressure test</h2>
      <p>Challenge your design with real-world failure modes.</p>
      <button type="button" onClick={onRequestPressure} disabled={disabled}>
        Request pressure test
      </button>
    </section>
  )
}
