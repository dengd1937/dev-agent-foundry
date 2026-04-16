#!/usr/bin/env python3
# Trigger:  PreToolUse — matcher: Bash
# Behavior: Soft REMINDER if `git commit` runs without a code-reviewer agent call
#           since the last commit. Never blocks — always exits 0.
# Disable:  export SKIP_REVIEW_CHECK=1  OR  chmod -x this file

import json
import os
import re
import sys

REVIEW_KEYWORD = "reviewer"

SOURCE_EXTS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".mts", ".cts",
    ".go", ".rs", ".java", ".rb", ".cs", ".cpp", ".c", ".h", ".hpp",
    ".swift", ".kt", ".scala", ".dart", ".php", ".lua",
    ".vue", ".svelte", ".html", ".css", ".scss", ".sql",
}

EXEMPT_RE = re.compile(
    r"(tests?/|__tests__/|test_fixtures?/|spec/|scripts?/|\.env\.example)"
)

GIT_COMMIT_RE = re.compile(r"(^|[;&|]\s*)\s*git\s+commit\b")


def main() -> None:
    if os.environ.get("SKIP_REVIEW_CHECK") == "1":
        sys.exit(0)

    try:
        payload = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    if payload.get("tool_name") != "Bash":
        sys.exit(0)

    cmd: str = payload.get("tool_input", {}).get("command", "")
    first_line = cmd.split("\n", 1)[0]
    if not GIT_COMMIT_RE.search(first_line):
        sys.exit(0)

    transcript: str = payload.get("transcript_path", "")
    if not transcript or not os.path.isfile(transcript):
        sys.exit(0)

    try:
        with open(transcript) as f:
            lines = f.readlines()
    except Exception:
        sys.exit(0)

    # Walk transcript backwards: collect Write/Edit on source files and
    # Task(reviewer) calls. Stop when we hit the previous `git commit` Bash call.
    edited_files: list[str] = []
    saw_reviewer = False

    for raw in reversed(lines):
        try:
            entry = json.loads(raw)
        except Exception:
            continue

        if entry.get("type") != "assistant":
            continue

        content = entry.get("message", {}).get("content", [])
        if not isinstance(content, list):
            continue

        for block in content:
            if block.get("type") != "tool_use":
                continue

            name: str = block.get("name", "")
            inp: dict = block.get("input", {})

            if name == "Bash":
                bash_first = inp.get("command", "").split("\n", 1)[0]
                if GIT_COMMIT_RE.search(bash_first):
                    # Reached previous commit — window boundary
                    _emit(edited_files, saw_reviewer)
                    return

            elif name in ("Write", "Edit"):
                fp: str = inp.get("file_path", "")
                if _is_source(fp):
                    edited_files.append(fp)

            elif name == "Task":
                sub: str = str(inp.get("subagent_type", "")).lower()
                if REVIEW_KEYWORD in sub:
                    saw_reviewer = True

    _emit(edited_files, saw_reviewer)


def _is_source(path: str) -> bool:
    if not path or EXEMPT_RE.search(path):
        return False
    _, ext = os.path.splitext(path)
    return ext.lower() in SOURCE_EXTS


def _emit(files: list[str], saw_reviewer: bool) -> None:
    if saw_reviewer or not files:
        sys.exit(0)

    unique = list(dict.fromkeys(files))
    listed = "\n  - ".join(unique[:5])
    suffix = f"\n  ... and {len(unique) - 5} more" if len(unique) > 5 else ""

    print(
        "[hook] REMINDER: code-reviewer agent was not invoked since last commit.\n"
        f"Modified source files:\n"
        f"  - {listed}{suffix}\n"
        "Run code-reviewer (and python-reviewer / typescript-reviewer / security-reviewer as applicable).\n"
        "Override: export SKIP_REVIEW_CHECK=1",
        file=sys.stderr,
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
