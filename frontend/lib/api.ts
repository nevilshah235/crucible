/**
 * Fetch the Crucible backend with optional auth.
 * When the user is signed in, adds Authorization: Bearer <token> using the NextAuth session cookie.
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function getBackendToken(): Promise<string | null> {
  const res = await fetch("/api/auth/token", { credentials: "include" })
  if (!res.ok) return null
  const data = await res.json()
  return data.token ?? null
}

export type ApiRequestInit = RequestInit & { skipAuth?: boolean }

/**
 * Fetch the Crucible API. If the user is signed in, includes the JWT in Authorization header.
 */
export async function apiFetch(path: string, init: ApiRequestInit = {}): Promise<Response> {
  const { skipAuth, ...rest } = init
  const headers = new Headers(rest.headers)
  if (!skipAuth && typeof window !== "undefined") {
    const token = await getBackendToken()
    if (token) {
      headers.set("Authorization", `Bearer ${token}`)
    }
  }
  const url = path.startsWith("http") ? path : `${API_URL}${path}`
  return fetch(url, { ...rest, headers, credentials: "include" })
}

export { API_URL }
