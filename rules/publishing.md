# Publishing — MCP push procedure and idempotency

No CI in this phase. Publishing is an LLM session, using the Suunto MCP tool and the Liftosaur MCP
tool directly, following this procedure.

## Endurance sessions → Suunto MCP

1. **Push a rolling ~2-week window**, not the whole plan at once. The plan is meant to adapt to how
   training actually goes (see `rules/progression.md`), and pushing far-future sessions that will
   likely be revised is wasted work and watch clutter.
2. For each `endurance/*.md` file in the window:
   - Skip if `publish: false` is set in frontmatter (meeting-time walks tracked in-repo only).
   - Skip if `published.suunto` is already set **and** the file hasn't changed since — this is the
     idempotency check. There is no separate ledger; the frontmatter field is the source of truth.
   - Otherwise, push the body (the intervals.icu-syntax text after the frontmatter) via the MCP tool,
     using `frontmatter.name` as the guide name.
   - On success, write the current timestamp into `published.suunto` in that file.
3. If a push errors, check `rules/endurance-authoring.md` first — most failures are a syntax gotcha
   (bare `m` for meters, a rest step with no target, a missing description), not an MCP problem.

## Strength program → Liftosaur MCP

`strength/program.liftoscript` is pushed as a whole program, not per-session. Push it whenever it
changes materially (a new week appended, an exercise substitution, a maxes update) — check
`athlete/maxes.yml` is in sync with the Week 1 baseline numbers before the first push, since drift
between the two is easy to introduce silently.

## Idempotency — why frontmatter, not a separate ledger

`published.suunto: <ISO timestamp> | null` on every endurance file is the entire idempotency
mechanism. This deliberately avoids a separate "already pushed" list, which would drift from the
files it's tracking the moment someone edits a file without updating the ledger. If a file's body
changes after it was published, clear or update `published.suunto` as part of that edit so the next
publish pass knows to re-push it.

## What a future CI pipeline would need (out of scope now, but the layout anticipates it)

- A cron or webhook trigger on merge to run the same rolling-window push described above.
- The same frontmatter fields (`published.suunto`, `publish: false`) work unchanged as the
  idempotency and skip mechanism — no schema change needed to automate this later.
