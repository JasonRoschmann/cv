#!/usr/bin/env bash
set -uo pipefail
trap '' PIPE

INPUT="$(cat)"

# ────────────────────────────────────────────────────────────────────
# Command-Extraktion: python3 ist der praezise Primaerpfad.
# WICHTIG (Fix 2026-06-16): NICHT mehr fail-closed bei Parse-Fehlern.
# Auf Windows-git-bash kann `python3` nach einem Session-Resume auf den
# nicht-funktionalen WindowsApps-Store-Stub resolven (exit 1, keine Ausgabe).
# Frueher blockte das JEDEN Bash-Befehl ("Hook-Input konnte nicht ... geparst")
# und brickte die ganze Session. Jetzt: Fallback auf Roh-Input-Scan, damit die
# Destruktiv-Blockliste TROTZDEM greift (rm -rf/sudo/etc. stehen im JSON-Text),
# ohne harmlose Befehle zu blockieren. Backup: pre-bash-guard.sh.bak-failclosed-20260616
# ────────────────────────────────────────────────────────────────────
CMD=""
# 2026-07-01: python3 kann auf Windows nach Store-Deinstallation als
# nicht-funktionaler Alias-Stub auf PATH bleiben — `command -v` findet ihn,
# die Ausfuehrung schlaegt aber fehl (exit != 0, Store-Fehlermeldung). Deshalb
# echte Ausfuehrbarkeit testen statt nur Existenz, mit Fallback auf `python`.
PYBIN=""
for _pycand in python3 python; do
  if command -v "$_pycand" >/dev/null 2>&1 && "$_pycand" -c "" >/dev/null 2>&1; then
    PYBIN="$_pycand"
    break
  fi
done
if [ -n "$PYBIN" ]; then
  CMD="$(printf '%s' "$INPUT" | "$PYBIN" -c '
import sys, json
try:
    data = json.load(sys.stdin)
    cmd = data.get("tool_input", {}).get("command") or data.get("command", "")
    if cmd is None:
        cmd = ""
    print(cmd)
except Exception:
    sys.exit(1)
' 2>/dev/null)" || CMD=""
fi

# Fallback: konnte das Command nicht praezise extrahiert werden, scanne den
# Roh-Input (enthaelt das Command als JSON-String). Lieber gegen den Rohtext
# pruefen als die Session lahmlegen.
SCAN="$CMD"
if [ -z "$(printf '%s' "$SCAN" | tr -d '[:space:]')" ]; then
  SCAN="$INPUT"
fi

# ────────────────────────────────────────────────────────────────────
# Helper: Denial-Response senden und exiten
# ────────────────────────────────────────────────────────────────────
deny() {
  local msg="$1"
  local esc_msg="${msg//\"/\\\"}"
  printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"%s"}}\n' "$esc_msg" 2>/dev/null || true
  exit 0
}

# ────────────────────────────────────────────────────────────────────
# BLOCK-LIST — nur wirklich irreversible / destruktive Befehle
# ────────────────────────────────────────────────────────────────────

# 1. Recursive grep → use rg (Performance + Konsistenz)
if printf '%s' "$SCAN" | grep -Eq '(^|[[:space:]]|;|&&|\|\|)grep[[:space:]]+(-[a-zA-Z]*[rR][a-zA-Z]*([[:space:]]|$)|--recursive\b|--include=.*-r)'; then
  deny "Nutze rg statt recursive grep (Performance, klarere Ausgabe)."
fi

# 2. Irreversible Datei-Destruktion (rm -rf / rm -r / rm --recursive / rm --force)
if printf '%s' "$SCAN" | grep -Eq '\brm[[:space:]]+(-[a-zA-Z]*[rRfF][a-zA-Z]*([[:space:]]|$)|--recursive\b|--force\b)'; then
  deny "Recursive/forced rm geblockt. Bei Bedarf human approval anfordern."
fi

# 3. Disk-Level-Destruktion (dd / mkfs / shred / wipefs)
if printf '%s' "$SCAN" | grep -Eq '\b(dd[[:space:]]+[^|]*\bof=|mkfs\.[a-z0-9]+|shred[[:space:]]+-|wipefs\b)'; then
  deny "Disk-Level-Destruktion geblockt (dd/mkfs/shred/wipefs)."
fi

# 4. Privilege Escalation
if printf '%s' "$SCAN" | grep -Eq '(^|[[:space:]]|;|&&|\|\|)(sudo|doas)([[:space:]]|$)|[[:space:]]su[[:space:]]+-'; then
  deny "Privilege Escalation (sudo/doas/su) geblockt."
fi

# 5. Remote Code Execution (curl/wget piped to shell)
if printf '%s' "$SCAN" | grep -Eq '(curl|wget|fetch|iwr|Invoke-WebRequest)[^|]*\|[[:space:]]*(bash|sh|zsh|fish|pwsh|powershell|python[23]?|ruby|perl|node)'; then
  deny "Pipe-to-Shell-Pattern geblockt (Remote-Code-Execution-Risiko)."
fi

# 6. Infrastructure-Destruktion
if printf '%s' "$SCAN" | grep -Eq '\b(terraform[[:space:]]+destroy|kubectl[[:space:]]+delete|helm[[:space:]]+uninstall|pulumi[[:space:]]+destroy)\b'; then
  deny "Infrastructure-Destruktion geblockt (terraform/kubectl/helm/pulumi)."
fi

# 7. Docker Bulk-Destruktion
if printf '%s' "$SCAN" | grep -Eq '\bdocker[[:space:]]+(system[[:space:]]+prune[[:space:]]+.*-a|volume[[:space:]]+prune|image[[:space:]]+prune[[:space:]]+.*-a)'; then
  deny "Docker Bulk-Destruktion geblockt (system/volume/image prune -a)."
fi

# 8. World-writable Permissions (Security-Hole)
if printf '%s' "$SCAN" | grep -Eq '\bchmod[[:space:]]+(-R[[:space:]]+)?(777|a\+w)\b'; then
  deny "chmod 777 geblockt (erzeugt unsichere Permissions)."
fi

# 9. Device-File-Writes
if printf '%s' "$SCAN" | grep -Eq '>[[:space:]]*/dev/(sda|sdb|nvme|disk|mem|kmem)'; then
  deny "Direkter Write auf Device-File geblockt."
fi

# 10. Fork-Bomb Pattern
if printf '%s' "$SCAN" | grep -Eq ':\(\)\{|fork.*fork|while[[:space:]]+true.*&'; then
  deny "Fork-Bomb-aehnliches Pattern geblockt."
fi

# ────────────────────────────────────────────────────────────────────
# Default: Allow
# ────────────────────────────────────────────────────────────────────
printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}\n' 2>/dev/null || true
exit 0
