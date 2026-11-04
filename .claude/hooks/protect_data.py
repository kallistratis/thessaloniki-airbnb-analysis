"""PreToolUse hook: keep the raw files in data/ unchanged (CLAUDE.md rules).

- Edit / Write / NotebookEdit on a file in data/ -> denied
- Read on a file in data/ -> denied (inspect the CSVs with pandas instead)
- Bash commands that delete, move or write files in data/ -> denied

data_clean/ is not affected.
"""
import json
import os
import re
import sys

try:
    payload = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
tool = payload.get("tool_name", "")
tool_input = payload.get("tool_input", {}) or {}


def windows_path(path):
    """Turn a Git Bash path like /d/VS code/... into D:/VS code/..."""
    m = re.match(r"^/([a-zA-Z])(/|$)(.*)", path or "")
    return f"{m.group(1).upper()}:/{m.group(3)}" if m and os.name == "nt" else path


project_dir = windows_path(os.environ.get("CLAUDE_PROJECT_DIR") or payload.get("cwd") or os.getcwd())
data_dir = os.path.normcase(os.path.realpath(os.path.join(project_dir, "data")))


def in_data_dir(path):
    if not path:
        return False
    path = windows_path(path)
    if not os.path.isabs(path):
        path = os.path.join(windows_path(payload.get("cwd") or project_dir), path)
    full = os.path.normcase(os.path.realpath(path))
    return full == data_dir or full.startswith(data_dir + os.sep)


def deny(reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    }))
    sys.exit(0)


if tool in ("Edit", "Write", "NotebookEdit"):
    path = tool_input.get("file_path") or tool_input.get("notebook_path")
    if in_data_dir(path):
        deny("CLAUDE.md: never change the files in data/. Work on the _clean copies "
             "and export to data_clean/ instead.")

elif tool == "Read":
    if in_data_dir(tool_input.get("file_path")):
        deny("CLAUDE.md: do not open the raw files with Read. Inspect them with pandas "
             "(head(), sample(), info(), column_summary()).")

elif tool == "Bash":
    command = tool_input.get("command", "")
    # a path inside data/ (not data_clean/)
    data_path = r"(?<![\w.-])(?:\./)?data[/\\]"
    if re.search(data_path, command):
        writes = [
            r"\b(rm|rmdir|del|mv|truncate|tee|shred|unlink)\b",
            r"\bsed\s+(-\w*\s+)*-i",
            r"\b(Remove-Item|Move-Item|Rename-Item|Set-Content|Add-Content|Out-File|Clear-Content)\b",
            r">{1,2}\s*\\?[\"']?" + data_path,
            r"\.to_(csv|parquet|excel|pickle|json|feather|hdf)\(\s*[rf]?\\?[\"']" + data_path,
            r"open\(\s*[rf]?\\?[\"']" + data_path + r"[^\"']*\\?[\"']\s*,\s*\\?[\"'][wax+]",
        ]
        if any(re.search(p, command) for p in writes):
            deny("CLAUDE.md: never change the files in data/. This command would delete, "
                 "move or write a file there. Write results to data_clean/ instead.")

sys.exit(0)
