#!/usr/bin/env bash
set -euo pipefail

# Loop-prevention (Claude Code hook contract, 2026-05-22): if we are already
# inside a Stop-hook continuation loop (stop_hook_active=true), return success
# immediately so this gate cannot re-block indefinitely. Without this, a stale
# validation-status.json would block every single Stop attempt forever.
INPUT="$(cat 2>/dev/null || true)"
case "$INPUT" in
  *'"stop_hook_active":true'*|*'"stop_hook_active": true'*) exit 0 ;;
esac

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
STATUS="$ROOT/.claude/runtime/validation-status.json"

if [ ! -f "$STATUS" ]; then
  # WARN-ONLY (2026-05-23): never block the turn. Emit a non-blocking hint instead
  # of {"decision":"block"} so concluding work is always possible.
  printf '{"systemMessage":"Hinweis: Noch keine Validierung gelaufen (.claude/runtime/validation-status.json fehlt). Turn wird NICHT blockiert."}\n'
  exit 0
fi

SUMMARY="$ROOT/.claude/runtime/validation-summary.md"

# Parse failures AND filter out informational-only checks (lint, build, typecheck).
# These are explicitly marked non-blocking in post-edit-validate.sh (line 104:
# "javascript lint (informational only — does not gate)"). Gating on them here
# would contradict that policy.
BLOCKING_FAILED=$(python3 - "$STATUS" "$SUMMARY" <<'PY'
import sys, json, re
status_path, summary_path = sys.argv[1], sys.argv[2]

try:
    with open(status_path, encoding="utf-8") as f:
        total_failed = json.load(f).get('failed', 0)
except Exception:
    print(0); sys.exit(0)

if total_failed == 0:
    print(0); sys.exit(0)

# Read summary, count FAILs that are NOT in the informational allowlist.
INFORMATIONAL = {"javascript lint", "javascript build", "javascript typecheck",
                 "python lint", "python typecheck"}
blocking = 0
try:
    # encoding explizit: Summary enthaelt em-dash (—); Windows-Default cp1252
    # zerlegt ihn und die FAIL-Regex matcht nie (Warnung blieb stumm).
    with open(summary_path, encoding="utf-8") as f:
        for line in f:
            m = re.match(r'-\s*FAIL\s*[—–-]\s*(.+?)\s*$', line)
            if m and m.group(1).strip() not in INFORMATIONAL:
                blocking += 1
except Exception:
    # If we can't parse, fall back to raw count (safer to block than allow).
    blocking = total_failed
print(blocking)
PY
)

if [ "$BLOCKING_FAILED" != "0" ]; then
  # WARN-ONLY (2026-05-23): surface failures but never block the turn.
  printf '{"systemMessage":"Hinweis: %s blockierende Validierungs-Checks rot (.claude/runtime/validation-summary.md). Turn wird NICHT blockiert."}\n' "$BLOCKING_FAILED"
  exit 0
fi

# Success: exit 0 with empty stdout.
# Claude Code Stop-Hook schema only knows {"decision":"block","reason":...} for blocking.
# An "allow" payload is not a valid value -> the hook system treats it as schema error
# (cosmetic warning) and falls through to "allow" anyway. Cleaner: emit nothing.
exit 0
