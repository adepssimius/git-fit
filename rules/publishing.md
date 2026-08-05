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

## Endurance sessions → suuntool MCP

**The body is not what gets pushed.** An earlier version of this file said to "push the body (the
intervals.icu-syntax text)" directly. That was never true: `suuntool` is byte-transparent —
`guides_upload` sends whatever zip bytes it is handed and never opens or validates the archive.
The watch wants a `guide.json` step tree in absolute wire units, so the markdown has to be compiled
and packed first, by scripts in this repo:

```bash
python3 scripts/compile_guide.py endurance/2026-08-04-easy-strides.md   # -> guide.json
python3 scripts/pack_guide.py    endurance/2026-08-04-easy-strides.md --base64
```

Then pass that base64 to `mcp__suuntool__guides_upload`. `suuntool` needs `--allow-write`.

1. **Push a rolling ~2-week window**, not the whole plan at once. The plan is meant to adapt to how
   training actually goes (see `rules/progression.md`), and pushing far-future sessions that will
   likely be revised is wasted work and watch clutter.
2. For each `endurance/*.md` file in the window:
   - Skip if `publish:` is false in frontmatter (meeting-time walks tracked in-repo only, and the
     race file). **Compare case-insensitively** — the repo contains both `false` and `False`, and a
     case-sensitive check silently publishes ten sessions that opted out. `compile_guide.py`
     already refuses these; don't reintroduce the check by hand.
   - Skip if `published.suunto` is already set **and** the file hasn't changed since — this is the
     idempotency check. There is no separate ledger; the frontmatter field is the source of truth.
     The packer is deterministic (fixed mtime, stable JSON serialisation), so "has this changed" is
     a plain `sha256` comparison of the archive, not a judgment call.
   - Otherwise compile, pack, and upload.
   - On success, write the current timestamp into `published.suunto` in that file.
3. If compilation errors, check `rules/endurance-authoring.md` first — most failures are a syntax
   gotcha (bare `m` for meters, a rest step with no target), not a tooling problem.
4. **`owner` is deliberately not set** in either `manifest.json` or `guide.json`. The server echoes
   back `"Suunto"` regardless of what is uploaded, so any value is fiction. If a future server build
   requires the key to be present, set `OWNER` in `scripts/compile_guide.py` — it must then match in
   both files or the archive is rejected before upload.

### RESOLVED 2026-08-05: the trainer rides publish fine

This section used to say the nine `sport: Ride` sessions could not be published, because they
targeted `%FTP` and `bike.ftp_w` is null. That was fixed when the ride files were rewritten to
HR bands (`- 70m Z2 HR 85-95rpm`, `- 10m 65-72% HR 85rpm`), which the compiler resolves from the
LTHR-based zone table. All nine compile and the 08-06 ride is live (guide `vnsbcek5`).

**Give every block a section header.** The ride bodies originally had *no* headers at all — just
bare `- ` steps — so every step compiled to the fallback title and the watch showed three steps
all called `Step 1`. Headers added 2026-08-05 (`Warmup` / `Z2 base` / `Cooldown`, with `Z2 base`
added to `TITLE_RULES` as `Z2 BASE`). A missing header is not a compile error, so nothing catches
this but reading the compiled output before pushing — do that.

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
