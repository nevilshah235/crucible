import { getToken } from "next-auth/jwt"
import { NextRequest, NextResponse } from "next/server"

/** Returns the raw NextAuth JWT so the frontend can send it to the Crucible backend. */
export async function GET(req: NextRequest) {
  const token = await getToken({
    req,
    secret: process.env.NEXTAUTH_SECRET,
  })
  if (!token) {
    return NextResponse.json({ token: null }, { status: 401 })
  }
  // We don't have the raw JWT string in getToken result; getToken returns the decoded payload.
  // So we need another way. NextAuth stores the JWT in the cookie. We can read the cookie and
  // return it so the client can send it in Authorization: Bearer <cookie-value>.
  const cookieName =
    process.env.NODE_ENV === "production"
      ? "__Secure-next-auth.session-token"
      : "next-auth.session-token"
  const cookie = req.cookies.get(cookieName)?.value ?? null
  if (!cookie) {
    return NextResponse.json({ token: null }, { status: 401 })
  }
  return NextResponse.json({ token: cookie })
}
