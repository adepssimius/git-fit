#!/bin/bash
# Cloud environment setup for git-fit — provisions the suuntool MCP server.
#
# ---------------------------------------------------------------------------
# PARTLY SUPERSEDED — read this before pasting. Recovered onto master
# 2026-08-10 from branch claude/mcp-suuntool-fork-tdogtn, which was about to be
# deleted and was the only place this existed. Kept because nothing else in the
# repo records how the cloud environment is provisioned, and losing it means
# rebuilding that knowledge from scratch the next time the environment is
# rebuilt. It is preserved verbatim below rather than rewritten, because the
# current environment was configured by hand and the exact steps that produced
# `/usr/local/bin/suuntool-guides-preview` are not known here — do not assume
# the body is current where this header contradicts it.
#
# STILL CURRENT, and recorded nowhere else:
#   - Guides support (guides_upload, the whole endurance publishing path in
#     rules/publishing.md) is an UNMERGED upstream PR, tajchert/suuntool#4. A
#     stock `go install ...@latest` builds main and has no guides_* tools.
#   - Network access: Custom + default package managers, plus
#     api.sports-tracker.com and 247.sports-tracker.com. Liftosaur is
#     deliberately NOT allowlisted — see the note below for why.
#   - The binary must exist before Claude Code launches, which is why this is a
#     setup script and not a SessionStart hook.
#
# CHANGED since this was written:
#   - The MCP server is now invoked as `/usr/local/bin/suuntool-guides-preview`
#     (see .mcp.json), not `suuntool`. This script still builds/installs
#     `suuntool`; the install path and binary name need updating before reuse.
#   - Session handling has moved to .claude/scripts/suuntool-session.sh, which
#     .mcp.json runs at server start. It builds session.json from
#     SUUNTOOL_SESSION_KEY (+ optional SUUNTOOL_EMAIL / USERNAME / USER_KEY /
#     COUNTRY / OFFSET_MS). That replaces the SUUNTOOL_SESSION_JSON blob and the
#     SUUNTO_EMAIL/SUUNTO_PASSWORD login fallback in the "Suunto session"
#     section at the bottom of this file — prefer the script, which keeps the
#     account password out of the environment entirely.
# ---------------------------------------------------------------------------
#
# This file is NOT read by anything automatically. Paste its contents into the
# Setup script field of the cloud environment at claude.ai/code. It lives here
# so the thing you pasted is version-controlled and reviewable.
#
# Companion settings for that same environment:
#
#   Network access: Custom, "also include default package managers" checked,
#     api.sports-tracker.com
#     247.sports-tracker.com
#   (Liftosaur is NOT listed — as a claude.ai custom connector its traffic goes
#   through Anthropic's servers, not the session network, so an allowlist entry
#   would do nothing.)
#
#   Environment variables:
#     SUUNTOOL_SESSION_JSON={"sessionkey":"...","username":"...","email":"...",...}
#   i.e. the contents of ~/.config/suuntool/session.json from a machine where
#   you have run `suuntool login`, on a single line.
#
# Setup scripts must exit zero or the session fails to start, so every step
# that can fail without making the session useless is guarded.

set -uo pipefail

# --- suuntool, built from the guides PR -------------------------------------
# Guide support (guides_upload, the whole endurance publishing path in
# rules/publishing.md) is unmerged upstream and lives in tajchert/suuntool#4.
# A stock `go install ...@latest` builds main and has no guides_* tools at all,
# so the PR ref is the thing to build until it lands.
SUUNTOOL_PR=4
SUUNTOOL_SRC=/opt/suuntool-src

# A build is usable only if it has the guides command; a stock main-branch
# binary passes `command -v` and then fails at publish time on a missing tool.
suuntool_usable() {
  command -v suuntool >/dev/null 2>&1 && suuntool guides --help >/dev/null 2>&1
}

# Preferred: a prebuilt linux/amd64 tarball, which turns a ~1min Go build into
# a couple of seconds. Set SUUNTOOL_TARBALL_URL in the environment once you
# publish one from the fork. Two delivery notes, both load-bearing:
#   - raw.githubusercontent.com is on the default Trusted list and is served by
#     the security proxy, so a committed file always works.
#   - a GitHub *release asset* goes through the GitHub proxy, which scopes
#     requests to repositories attached to the session. An unattached repo is
#     documented to 403 here. If that bites, the source build below still runs.
if [ -n "${SUUNTOOL_TARBALL_URL:-}" ] && ! suuntool_usable; then
  if curl -fsSL --max-time 120 "$SUUNTOOL_TARBALL_URL" -o /tmp/suuntool.tar.gz &&
     tar -xzf /tmp/suuntool.tar.gz -C /usr/local/bin suuntool; then
    chmod +x /usr/local/bin/suuntool
  else
    echo "cloud-setup: prebuilt tarball unavailable, falling back to a source build" >&2
    rm -f /usr/local/bin/suuntool
  fi
  rm -f /tmp/suuntool.tar.gz
fi

# Fallback: build the guides PR from source. Unmerged upstream, so a stock
# `go install ...@latest` builds main and has no guides_* tools at all.
if ! suuntool_usable; then
  if git clone --depth 1 https://github.com/tajchert/suuntool "$SUUNTOOL_SRC" &&
     git -C "$SUUNTOOL_SRC" fetch --depth 1 origin "refs/pull/${SUUNTOOL_PR}/head:guides" &&
     git -C "$SUUNTOOL_SRC" checkout guides; then
    ( cd "$SUUNTOOL_SRC" && go build -trimpath -ldflags="-s -w" -o /usr/local/bin/suuntool . ) ||
      echo "cloud-setup: suuntool build failed; the suuntool MCP will not start" >&2
  else
    echo "cloud-setup: could not fetch tajchert/suuntool PR ${SUUNTOOL_PR}" >&2
  fi
fi

# Fail loudly here rather than at 6am when the brief asks for sleep data.
suuntool_usable ||
  echo "cloud-setup: no usable suuntool with guides support; publishing will fail" >&2

# --- Suunto session ---------------------------------------------------------
# The MCP server loads this file once at startup and never re-auths, so it has
# to exist before Claude Code launches. That is exactly what a setup script is
# for; a SessionStart hook would run after the server had already given up.
if [ -n "${SUUNTOOL_SESSION_JSON:-}" ]; then
  mkdir -p /root/.config/suuntool
  ( umask 077; printf '%s' "$SUUNTOOL_SESSION_JSON" > /root/.config/suuntool/session.json )
elif [ -n "${SUUNTO_EMAIL:-}" ] && [ -n "${SUUNTO_PASSWORD:-}" ]; then
  # Fallback: a real login. Self-heals when a session key expires, at the cost
  # of keeping the account password in the environment config.
  printf '%s' "$SUUNTO_PASSWORD" |
    suuntool login --email "$SUUNTO_EMAIL" --password-stdin >/dev/null 2>&1 ||
    echo "cloud-setup: suuntool login failed" >&2
else
  echo "cloud-setup: no Suunto credentials in the environment; suuntool tools will return AUTH_EXPIRED" >&2
fi

exit 0
