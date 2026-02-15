import type { NextAuthOptions } from "next-auth"
import GoogleProvider from "next-auth/providers/google"

export const authOptions: NextAuthOptions = {
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID ?? "",
      clientSecret: process.env.GOOGLE_CLIENT_SECRET ?? "",
    }),
  ],
  session: {
    strategy: "jwt",
    maxAge: 30 * 24 * 60 * 60, // 30 days
  },
  callbacks: {
    jwt({ token, user }) {
      if (user) {
        token.sub = user.id
        token.email = user.email ?? undefined
        token.name = user.name ?? undefined
        token.picture = user.image ?? undefined
      }
      return token
    },
    session({ session, token }) {
      if (session.user) {
        session.user.id = token.sub ?? ""
        session.user.email = token.email ?? null
        session.user.name = token.name ?? null
        session.user.image = token.picture ?? null
      }
      return session
    },
  },
  pages: {
    signIn: "/",
  },
}
