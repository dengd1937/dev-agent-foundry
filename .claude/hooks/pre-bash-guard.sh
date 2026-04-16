#!/usr/bin/env bash
# Trigger:  PreToolUse — matcher: Bash
# Behavior: BLOCKS dangerous git commands and wrong package manager usage.
# Disable:  chmod -x .claude/hooks/pre-bash-guard.sh

set -euo pipefail
source "$(dirname "${BASH_SOURCE[0]}")/lib/utils.sh"

INPUT=$(cat)
CMD=$(json_get "$INPUT" "tool_input.command")

[[ -z "$CMD" ]] && exit 0

# For git subcommand rules, only inspect the first line of the command.
# Heredoc bodies (commit messages, script content) live on subsequent lines
# and must not be scanned — they describe past actions, not current invocations.
FIRST_LINE=$(printf '%s' "$CMD" | head -1)

# Anchor pattern for multi-statement lines: match git/rm/pip only as actual
# invocations (start of command, or after && || ; |), not inside string literals.
INVOKE='(^|[;&|]\s*)\s*'

# ── Rule 1: No --no-verify on git commit ──────────────────────────────────────
if echo "$FIRST_LINE" | grep -qE "${INVOKE}git\s+commit.*--no-verify"; then
    log_block "--no-verify skips pre-commit hooks. Fix the failing hook instead of bypassing it."
    exit 2
fi

# ── Rule 2: No force-push to main or master ───────────────────────────────────
if echo "$FIRST_LINE" | grep -qE "${INVOKE}git\s+push.*(--force\b|-f\b)" && \
   echo "$FIRST_LINE" | grep -qE '\b(main|master)\b'; then
    log_block "Force-pushing to main/master is not allowed. Use a feature branch, or ask the user to confirm."
    exit 2
fi

# ── Rule 3: No git reset --hard ───────────────────────────────────────────────
if echo "$FIRST_LINE" | grep -qE "${INVOKE}git\s+reset\s+--hard"; then
    log_block "git reset --hard can destroy uncommitted changes. Stash or commit first, or ask the user to confirm."
    exit 2
fi

# ── Rule 4: No catastrophic rm -rf ────────────────────────────────────────────
# Block only when the dangerous target (/ ~ * ..) is the direct argument.
if echo "$CMD" | grep -qE "${INVOKE}rm\s+-[rf]{1,2}\s+(\/|~|\*|\.\.)"; then
    log_block "Potentially catastrophic rm -rf. Use a precise relative path instead of /, ~, *, or ../"
    exit 2
fi

# ── Rule 5: Wrong package manager (Python projects only) ─────────────────────
if is_python_project; then
    if echo "$CMD" | grep -qE "${INVOKE}(pip\s+install|poetry\s+add|conda\s+install|uv\s+pip\s+install)"; then
        log_block "Use 'uv add <package>' instead. pip/poetry/conda/uv pip install do not update pyproject.toml automatically."
        exit 2
    fi
fi

exit 0
