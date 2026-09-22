#!/usr/bin/env bash
set -uo pipefail
trap '' PIPE

# Opt-Out: Marker-Datei im Projekt deaktiviert alle Hook-Validierungen.
# Stdin vorher leeren, sonst broken pipe im Caller.
_PROJ="${CLAUDE_PROJECT_DIR:-$(pwd)}"
if [ -f "$_PROJ/.claude/hooks-disabled" ] || [ -f "$_PROJ/.claude-hooks-disabled" ]; then
  cat >/dev/null 2>&1 || true
  exit 0
fi

ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
RUNTIME_DIR="$ROOT/.claude/runtime"
mkdir -p "$RUNTIME_DIR"
LOG="$RUNTIME_DIR/post-edit-validate.log"
SUMMARY="$RUNTIME_DIR/validation-summary.md"
STATUS="$RUNTIME_DIR/validation-status.json"
: > "$LOG"

append() { printf '%s\n' "$1" | tee -a "$LOG" >/dev/null; }

passed=0; failed=0; checks=()
record_pass(){ passed=$((passed+1)); checks+=("PASS::$1"); }
record_fail(){ failed=$((failed+1)); checks+=("FAIL::$1"); }

run_check() {
  local name="$1"; shift
  append "==> $name"
  if "$@" >>"$LOG" 2>&1; then
    append "PASS: $name"
    record_pass "$name"
    return 0
  else
    append "FAIL: $name"
    record_fail "$name"
    return 1
  fi
}

# static policy checks
if ! command -v rg >/dev/null 2>&1; then
  append "FAIL: rg (ripgrep) not installed — static scans skipped"
  record_fail "rg availability"
else
  # Excludes use **/-anchored globs so nested vendor dirs (e.g. web/node_modules)
  # are skipped even outside a git repo, where rg does not auto-apply .gitignore.
  if rg -n -e '\b(TODO|FIXME)\b' -e '^\s*pass\s*(#.*)?$' -e '^\s*\.\.\.\s*$' . --glob '!**/node_modules/**' --glob '!**/.git/**' --glob '!**/.next/**' --glob '!**/dist/**' --glob '!**/build/**' --glob '!**/*.md' --glob '!**/*.mdx' --glob '!**/*.rst' --glob '!**/*.txt' --glob '!**/.claude/**' --glob '!**/post-edit-validate.sh' >>"$LOG" 2>&1; then
    append "FAIL: placeholder scan"; record_fail "placeholder scan"
  else
    append "PASS: placeholder scan"; record_pass "placeholder scan"
  fi

  # Dependency pinning: only real manifests (package.json). Lockfiles & vendored
  # node_modules legitimately carry transitive ^/~ ranges and are not authored here.
  if rg -n '"[^"]+"\s*:\s*"[~^][^"]+"' . --glob '**/package.json' --glob '!**/node_modules/**' >>"$LOG" 2>&1; then
    append "FAIL: dependency pinning scan"; record_fail "dependency pinning scan"
  else
    append "PASS: dependency pinning scan"; record_pass "dependency pinning scan"
  fi

  if git rev-parse --git-dir >/dev/null 2>&1; then
    if git ls-files | rg '(^|/)(\.env($|\.)|.*\.pem$)' >>"$LOG" 2>&1; then
      append "FAIL: secret tracking scan"; record_fail "secret tracking scan"
    else
      append "PASS: secret tracking scan"; record_pass "secret tracking scan"
    fi
  else
    append "SKIP: secret tracking scan (not a git repo)"; record_pass "secret tracking scan"
  fi
fi

# Entschlackt 2026-07-22: make test/lint/build, npm/pnpm lint/typecheck/build,
# pytest/mypy/ruff, go test und cargo liefen hier nach JEDEM Edit (bis 60s pro
# Turn). Tests/Builds laufen jetzt nur noch explizit (make test laut Protokoll).
# Original: post-edit-validate.sh.bak-heavy-20260722

{
  echo "# Validation summary"
  echo
  echo "- Passed checks: $passed"
  echo "- Failed checks: $failed"
  echo
  echo "## Checks"
  for item in "${checks[@]}"; do
    status="${item%%::*}"; name="${item#*::}"; echo "- $status — $name"
  done
  echo
  echo "## Log"
  echo "See .claude/runtime/post-edit-validate.log"
} > "$SUMMARY"

printf '{"passed": %s, "failed": %s}\n' "$passed" "$failed" > "$STATUS"

cat "$SUMMARY"
exit 0
