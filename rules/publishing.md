# Publishing — MCP push procedure and idempotency

No CI in this phase. Publishing is an LLM session, using the Suunto MCP tool and the Liftosaur MCP
tool directly, following this procedure.

**Liftosaur MCP status: connected and in use** (`.mcp.json`, project-scoped, `https://www.liftosaur.com/mcp`).
`strength/program.liftoscript` is live in the account as **"Ghost Train Block"** (program id
`haqytaxt`), pushed via `mcp__liftosaur__update_program`. Before writing or editing that file,
call `mcp__liftosaur__get_liftoscript_reference` — Liftoscript has sharp edges that don't match
intuition from other DSLs (see `strength/notes.md` for the specific ones that bit us: a timed hold
needs an explicit rep count before the duration — `3x1 30s|30s`, not `3x30s|30s` — and cross-week
carry-forward could not be made to work reliably, so every week is written out in full).

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

`strength/program.liftoscript` is pushed as a whole program (`mcp__liftosaur__update_program`,
`id: "haqytaxt"`), not per-session. Push it whenever it changes materially (a new week appended, an
exercise substitution, a real-weight correction from `athlete/maxes.yml`).

Before pushing:
1. `mcp__liftosaur__get_liftoscript_reference` if it's been a while — the syntax has non-obvious
   traps (see `strength/notes.md`).
2. `mcp__liftosaur__list_custom_exercises` if the edit introduces a new exercise name not in
   `mcp__liftosaur__list_exercises`'s built-in list — reuse an existing custom by exact name rather
   than creating a duplicate, or workout history linkage breaks.
3. Validate with `mcp__liftosaur__get_program_stats` (structural — catches parse errors, gives a
   volume/muscle-group sanity check) and spot-check at least one new/changed week with
   `mcp__liftosaur__run_playground` using real `complete_set(...)` commands, not just a bare
   request — a syntactically valid week can still resolve the wrong weight at runtime.
4. Push with `update_program`, then re-read with `mcp__liftosaur__get_program({id: "current"})` or
   `list_programs` to confirm the live version matches what was intended.
5. Keep the local `strength/program.liftoscript` byte-for-byte in sync with what's live — write the
   tool's returned `text` back to the file rather than assuming the push matched what was sent.

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
