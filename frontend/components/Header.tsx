"use client"

import Link from "next/link"
import { signIn, signOut, useSession } from "next-auth/react"

export function Header() {
  const { data: session, status } = useSession()

  return (
    <header style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "1rem", flexWrap: "wrap" }}>
      <Link href="/">Crucible</Link>
      <Link href="/admin">Admin</Link>
      {status === "loading" ? (
        <span>Loading…</span>
      ) : session?.user ? (
        <>
          <span style={{ marginLeft: "auto" }}>
            Signed in as {session.user.name ?? session.user.email ?? session.user.id}
          </span>
          <button type="button" onClick={() => signOut()}>
            Sign out
          </button>
        </>
      ) : (
        <button type="button" onClick={() => signIn("google")} style={{ marginLeft: "auto" }}>
          Sign in with Google
        </button>
      )}
    </header>
  )
}
