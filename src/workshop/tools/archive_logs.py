#!/usr/bin/env python3
"""Move old dated entries out of log/journal.md and log/decisions.md into one file per day.

Agents read the live log files; the full history cost ~180k tokens to read and was rarely needed. This keeps
only the newest `--keep` dates in each live file and moves every older `## YYYY-MM-DD …` entry, unchanged and
in order, to `log/archive/<journal|decisions>/YYYY-MM-DD.md` (appended if that file exists). Everything before
the first dated entry stays: the preamble, and in decisions.md the format block and the "In force" table.
Find an archived entry with `grep -rn '^## .*<title words>' log/`.

    uv run ws-archive-logs [--keep 1] [--dry-run] [--log DIR]
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

LOG = Path("log")  # relative to the repo root; --log DIR overrides
DATED = re.compile(r"## (\d{4}-\d\d-\d\d)")


def split(text: str) -> tuple[str, list[tuple[str, str]]]:
    """(everything before the first dated entry, [(date, entry text)])."""
    parts = re.split(r"(?m)^(?=## )", text)
    head, entries = parts[0], []
    for p in parts[1:]:
        m = DATED.match(p)
        if m:
            entries.append((m.group(1), p))
        elif entries:  # an undated heading after dated ones belongs to the entry before it
            entries[-1] = (entries[-1][0], entries[-1][1] + p)
        else:
            head += p
    return head, entries


def archive(name: str, keep: int, dry: bool) -> None:
    path = LOG / f"{name}.md"
    head, entries = split(path.read_text())
    dates = sorted({d for d, _ in entries})
    kept_dates = set(dates[-keep:]) if keep > 0 else set()
    moved: dict[str, str] = {}
    live = head
    for d, e in entries:
        if d in kept_dates:
            live += e
        else:
            moved[d] = moved.get(d, "") + e
    print(f"{name}: keep {sorted(kept_dates)}, move {len(moved)} days ({sum(map(len, moved.values())) // 1024} KB)")
    if dry:
        return
    out = LOG / "archive" / name
    out.mkdir(parents=True, exist_ok=True)
    for d, text in moved.items():
        f = out / f"{d}.md"
        prefix = f.read_text().rstrip("\n") + "\n\n" if f.exists() else f"# {name.capitalize()}, {d} (archived)\n\n"
        f.write_text(prefix + text.rstrip("\n") + "\n")
    path.write_text(live.rstrip("\n") + "\n")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--keep", type=int, default=1, help="newest dates to keep in the live file (default 1)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--log", type=Path, default=None, help="log directory (default ./log)")
    a = ap.parse_args()
    global LOG
    LOG = a.log or LOG
    for name in ("journal", "decisions"):
        archive(name, a.keep, a.dry_run)


if __name__ == "__main__":
    main()
