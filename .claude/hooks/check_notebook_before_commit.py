"""PreToolUse hook on `git commit`: the notebook must have been run after a restart.

CLAUDE.md: "Before committing, restart the kernel and run all cells, so that
every cell has its output."

If 01_data_cleaning.ipynb is part of the commit (staged, or changed and added
in the same command), check that:
- every non-empty code cell was run (execution_count is not None),
- the execution counts are 1, 2, 3, ... with no gaps (run once, after a restart),
- no cell has an error output.
"""
import json
import os
import re
import subprocess
import sys

NOTEBOOK = "01_data_cleaning.ipynb"

payload = json.load(sys.stdin)
command = (payload.get("tool_input") or {}).get("command", "")
if not re.search(r"\bgit\b[^|;&]*\bcommit\b", command):
    sys.exit(0)

project_dir = os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd()


def git(*args):
    return subprocess.run(["git", *args], cwd=project_dir, capture_output=True,
                          text=True, encoding="utf-8").stdout


staged = NOTEBOOK in git("diff", "--cached", "--name-only").split()
changed = NOTEBOOK in git("diff", "--name-only").split()
adds_in_command = bool(re.search(r"\bgit\s+add\b|\bcommit\b[^|;&]*\s(-a\w*|--all)\b", command))

versions = []
if staged:
    versions.append(("staged", git("show", ":" + NOTEBOOK)))
if changed and adds_in_command:
    with open(os.path.join(project_dir, NOTEBOOK), encoding="utf-8") as f:
        versions.append(("working copy", f.read()))
if not versions:
    sys.exit(0)

problems = []
for label, text in versions:
    cells = json.loads(text)["cells"]
    code = [(i, c) for i, c in enumerate(cells)
            if c["cell_type"] == "code" and "".join(c["source"]).strip()]
    not_run = [i for i, c in code if c.get("execution_count") is None]
    counts = [c["execution_count"] for i, c in code if c.get("execution_count") is not None]
    errors = [i for i, c in code for o in c.get("outputs", []) if o.get("output_type") == "error"]
    if not_run:
        problems.append(f"{label}: code cells without execution_count (not run): {not_run}")
    if counts and counts != list(range(1, len(counts) + 1)):
        problems.append(f"{label}: execution counts are {counts[:3]}...{counts[-3:]}, "
                        f"not 1..{len(counts)} (not one run after a restart)")
    if errors:
        problems.append(f"{label}: cells with an error output: {errors}")

if problems:
    reason = ("CLAUDE.md: before committing, restart the kernel and run all cells. "
              + " | ".join(problems)
              + " | Ask the user to Restart + Run All + Save in VS Code, then commit.")
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
sys.exit(0)
