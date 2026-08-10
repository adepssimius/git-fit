#!/usr/bin/env bash
# Materialize suuntool's session file from environment variables.
#
# Set these in the cloud environment's variable config:
#   SUUNTOOL_SESSION_KEY  (required) bearer key — THIS is the secret
#   SUUNTOOL_EMAIL        (optional) only needed for x-totp writes
#                                    (comments/reactions/edits); guides don't use it
#   SUUNTOOL_USERNAME     (optional) cosmetic, shown by `whoami`
#   SUUNTOOL_USER_KEY     (optional) cosmetic
#   SUUNTOOL_COUNTRY      (optional) cosmetic
#   SUUNTOOL_OFFSET_MS    (optional) server-clock offset for TOTP; leave unset
#                                    on an NTP-synced host (defaults to 0)
set -euo pipefail

# Mirrors internal/session.Path() exactly.
if [ -n "${SUUNTOOL_SESSION_FILE:-}" ]; then
  dest="$SUUNTOOL_SESSION_FILE"
elif [ -n "${XDG_CONFIG_HOME:-}" ]; then
  dest="$XDG_CONFIG_HOME/suuntool/session.json"
else
  dest="$HOME/.config/suuntool/session.json"
fi

if [ -z "${SUUNTOOL_SESSION_KEY:-}" ]; then
  echo "suuntool: SUUNTOOL_SESSION_KEY unset — skipping session setup." >&2
  echo "suuntool: authenticated commands will return AUTH_EXPIRED (exit 4)." >&2
  exit 0
fi

# Escape backslashes and double quotes so the values can't break the JSON.
esc() { printf '%s' "${1:-}" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'; }

offset="${SUUNTOOL_OFFSET_MS:-0}"
case "$offset" in
  ''|*[!0-9-]*) echo "suuntool: SUUNTOOL_OFFSET_MS must be an integer, got '$offset'" >&2; exit 1 ;;
esac

mkdir -p "$(dirname "$dest")"
chmod 700 "$(dirname "$dest")" 2>/dev/null || true
umask 077
cat > "$dest" <<EOF
{
  "sessionkey": "$(esc "${SUUNTOOL_SESSION_KEY}")",
  "username": "$(esc "${SUUNTOOL_USERNAME:-}")",
  "email": "$(esc "${SUUNTOOL_EMAIL:-}")",
  "userKey": "$(esc "${SUUNTOOL_USER_KEY:-}")",
  "country": "$(esc "${SUUNTOOL_COUNTRY:-}")",
  "server_time_offset_ms": ${offset},
  "saved_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
chmod 600 "$dest"
echo "suuntool: wrote session to $dest" >&2
