---
name: guided-changes
description: When making code changes, the agent explains every edit so the user learns as they go. Use when the user wants guided changes, wants to learn frontend (React, Next.js, components), or asks to be walked through each change.
---

# Guided Changes (Learn While Coding)

## When This Applies

Use this skill when the user:
- Wants to learn frontend (or any part of the stack) while building
- Asks to be guided through changes or have every change explained
- Is in a project where "explain every change" or "learning mode" was requested

## How to Behave

For **every** code change (file create, edit, or delete):

1. **Before or with the change:** State what you are about to do in one short sentence (e.g. "Adding a React component that will display the concept text").
2. **After the change:** In 2–4 bullet points, briefly explain:
   - **What** you changed (file and main idea)
   - **Why** it’s there (purpose in the flow)
   - **How** it works (one line on the mechanism, e.g. "This component receives `concept` as a prop and renders the title and body")
   - For **frontend** (JS/TS, React, Next.js, CSS): add one learning note (e.g. "In Next.js App Router, `page.tsx` is the UI for that route" or "We use `useState` here so the UI updates when the user submits").

Keep explanations short. No long tutorials unless the user asks. Prefer bullets over paragraphs.

## Frontend-Focused Notes

When the change touches frontend (components, pages, hooks, styling, API calls from the client):

- Name the pattern (e.g. "controlled input", "client component", "fetch in useEffect").
- Point to the file/line that "wires" things (e.g. "The page that uses this component is in `app/page.tsx`").
- If something is optional or could be done differently later, say so in one line (e.g. "We could later move this to a server component").

## What Not to Do

- Do not skip explanations for "obvious" edits when the user asked for guided changes.
- Do not dump long docs; keep each explanation scoped to the change you just made.
- Do not explain things the user didn’t ask about and that aren’t related to the current edit.