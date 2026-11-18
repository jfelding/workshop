"""Every project shows what its parts look like, so a person can tell which file is which.

    ws-check-pictures [--committed] PROJECT_DIR ...

Per project, after its parts are built:
- every ``exports/<part>.stl`` has ``exports/<part>.png`` beside it (``workshop.cad.export`` writes
  it; ``ws-preview`` makes one for an STL written some other way);
- ``README.md`` shows every one of those pictures, and at least one picture exists;
- with ``--committed`` (CI), every picture the README shows is tracked by git.
Exits 1 and lists what is missing.
"""
import re
import subprocess
import sys
from pathlib import Path

IMAGE = re.compile(r'!\[[^\]]*\]\(([^)\s]+)|<img[^>]*\bsrc="([^"]+)"')


def problems(project, committed=False):
    project = Path(project)
    readme = project / 'README.md'
    if not readme.exists():
        return [f'{project}: no README.md']
    text = readme.read_text()
    shown = [a or b for a, b in IMAGE.findall(text)]
    out = []
    for stl in sorted((project / 'exports').glob('*.stl')):
        png = stl.with_suffix('.png')
        rel = png.relative_to(project).as_posix()
        if not png.exists():
            out.append(f'{project}: {rel} missing (export with workshop.cad.export, or run ws-preview {stl.name})')
        if rel not in shown:
            out.append(f'{project}: README.md does not show {rel}')
    existing = [s for s in shown if (project / s).exists()]
    if not existing:
        out.append(f'{project}: README.md shows no picture of the thing (add ![...](exports/preview.png))')
    for s in shown:
        if not (project / s).exists() and not s.startswith('http'):
            out.append(f'{project}: README.md shows {s}, which does not exist')
    if committed and existing:
        tracked = subprocess.run(['git', 'ls-files', '--', *existing], cwd=project,
                                 capture_output=True, text=True).stdout.split()
        for s in existing:
            if Path(s).as_posix() not in tracked:
                out.append(f'{project}: {s} is not committed (git add it)')
    return out


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    committed = '--committed' in args
    dirs = [a for a in args if a != '--committed'] or ['.']
    found = [p for d in dirs for p in problems(d, committed)]
    print('\n'.join(found) if found else f'pictures ok: {", ".join(dirs)}')
    return 1 if found else 0


if __name__ == '__main__':
    sys.exit(main())
