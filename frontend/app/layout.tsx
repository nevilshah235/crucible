import type { Metadata } from "next"
import "./globals.css"

export const metadata: Metadata = {
  title: "Crucible",
  description: "Learn, quiz, design, get coach feedback. System design under pressure.",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
