#!/usr/bin/env python3
"""Ratchet on code file size: fail when a tracked code file passes LIMIT lines.

Files already over the limit are listed in file-size-allowlist.txt (repo root) with
their line count; they may shrink but not grow. `--update` only ever lowers
entries or drops them; raising or adding one is a deliberate hand edit.
Run from the repo root: `uv run ws-check-file-sizes` (standard library only).
"""

import subprocess
import sys
from pathlib import Path

LIMIT = 800
EXTENSIONS = {".py", ".rs", ".js", ".mjs", ".ts", ".html", ".css", ".sh"}
EXCLUDED_DIRS = {"vendor", "log", "target", "node_modules", "__pycache__"}
ALLOWLIST = Path("file-size-allowlist.txt")  # relative to the repo root; --allowlist=PATH overrides
HEADER = (
    "# Ratchet: code files over 800 lines may not grow past the count here. "
    "`ws-check-file-sizes --update` only lowers or drops entries; raise by hand.\n"
)


def is_code(path: str) -> bool:
    p = Path(path)
    return p.suffix in EXTENSIONS and not (set(p.parts[:-1]) & EXCLUDED_DIRS)


def count_lines(path: Path) -> int:
    """Line count the way `wc -l` does (number of newline bytes)."""
    return path.read_bytes().count(b"\n")


def read_allowlist(path: Path) -> tuple[dict[str, int], dict[str, str]]:
    """Return ({file: lines}, {file: trailing comment})."""
    limits: dict[str, int] = {}
    notes: dict[str, str] = {}
    if not path.exists():
        return limits, notes
    for raw in path.read_text().splitlines():
        body, _, comment = raw.partition("#")
        fields = body.split(None, 1)
        if not fields:
            continue
        limits[fields[1].strip()] = int(fields[0])
        if comment.strip():
            notes[fields[1].strip()] = comment.strip()
    return limits, notes


def check(counts: dict[str, int], allow: dict[str, int], limit: int = LIMIT) -> list[str]:
    """Problems for the given {file: lines} counts and allowlist."""
    problems = []
    for path, n in sorted(counts.items()):
        if path in allow:
            if n > allow[path]:
                problems.append(f"{path}: {n} lines, allowlist records {allow[path]} (grew)")
        elif n > limit:
            problems.append(f"{path}: {n} lines, over the {limit}-line limit")
    for path, n in sorted(allow.items()):
        if path not in counts:
            problems.append(f"{path}: stale allowlist entry (file no longer exists)")
        elif counts[path] <= limit:
            problems.append(
                f"{path}: stale allowlist entry ({counts[path]} lines, now within limit)"
            )
    return problems


def update(counts: dict[str, int], allow: dict[str, int], limit: int = LIMIT) -> dict[str, int]:
    """New allowlist: entries only lowered or dropped, never raised or added."""
    new = {}
    for path, recorded in allow.items():
        n = counts.get(path)
        if n is not None and n > limit:
            new[path] = min(n, recorded)
    return new


def write_allowlist(path: Path, allow: dict[str, int], notes: dict[str, str]) -> None:
    lines = [HEADER]
    for f, n in sorted(allow.items(), key=lambda kv: (-kv[1], kv[0])):
        note = f"  # {notes[f]}" if f in notes else ""
        lines.append(f"{n} {f}{note}\n")
    path.write_text("".join(lines))


def tracked_counts() -> dict[str, int]:
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    return {f: count_lines(Path(f)) for f in out.splitlines() if is_code(f) and Path(f).is_file()}


def main(argv: list[str] | None = None) -> int:
    global ALLOWLIST
    argv = sys.argv[1:] if argv is None else argv
    for a in argv:
        if a.startswith("--allowlist="):
            ALLOWLIST = Path(a.split("=", 1)[1])
    counts = tracked_counts()
    allow, notes = read_allowlist(ALLOWLIST)
    if "--update" in argv:
        write_allowlist(ALLOWLIST, update(counts, allow), notes)
        print(f"updated {ALLOWLIST}")
        return 0
    problems = check(counts, allow)
    if not problems:
        return 0
    print(f"File-size check failed ({LIMIT}-line limit):")
    for p in problems:
        print(f"  {p}")
    print(
        "Put new code in a new module/file rather than growing this one. If the file is\n"
        "genuinely one cohesive thing, raise its entry in the allowlist by\n"
        "hand and say why in the commit message. After shrinking a file, run with --update."
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
