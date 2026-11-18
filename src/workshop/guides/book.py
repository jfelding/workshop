"""Number a set of guide chapters, link them and write the HTML next to each other.

    from workshop.guides.book import Chapter, write_book
    write_book(out_dir, "Assembly guides", [
        Chapter("01-base", ch01, "Base and long axis", "Done"),
        Chapter("02-frame", ch02, "Frame", "Next"),
    ])

Each chapter module exposes build(nav) -> HTML (built with workshop.guides.style.page).
The index page is 00-start-here.html, with each chapter's status beside it.
"""
import os
from dataclasses import dataclass
from types import ModuleType

from .style import CSS

NAVCSS = '.nav{display:flex;justify-content:space-between;gap:12px;margin-bottom:18px;font-size:14px}.nav a{color:var(--ink);font-weight:600}' \
         '.next{border-top:3px solid var(--ink);margin-top:48px;padding-top:18px;font-size:20px;font-weight:700}.next a{color:var(--ink)}' \
         '.toc{list-style:none;padding:0;margin:0}.toc li{display:grid;grid-template-columns:64px minmax(0,1fr) auto;align-items:center;gap:10px 16px;border-top:3px solid var(--ink);padding:14px 0}' \
         '.toc .n{font-weight:700;font-size:44px;line-height:1;min-width:64px;white-space:nowrap}.toc a{color:var(--ink);font-weight:700;font-size:18px}' \
         '.toc .s{max-width:240px;border:2px solid var(--ink);padding:2px 10px;font-size:14px;font-weight:600;text-align:right}' \
         '@media(max-width:600px){.toc li{grid-template-columns:52px minmax(0,1fr)}.toc .n{font-size:36px;min-width:0}.toc .s{grid-column:2;max-width:none;justify-self:start;text-align:left}}'


@dataclass
class Chapter:
    file: str           # "01-base-and-long-axis" (the first two characters are its number)
    module: ModuleType  # has build(nav) -> html
    title: str
    status: str = ""


def _nav(chs, i):
    prev = f'<a href="{chs[i-1].file}.html">← {chs[i-1].file[:2]}</a>' if i > 0 else '<span></span>'
    nxt = f'<a href="{chs[i+1].file}.html">{chs[i+1].file[:2]} →</a>' if i < len(chs) - 1 else '<span></span>'
    return f'<div class="nav">{prev}<a href="00-start-here.html">00 start</a>{nxt}</div>'


def _foot(chs, i):
    if i < len(chs) - 1:
        c = chs[i+1]
        return f'<div class="next"><a href="{c.file}.html">Next: {c.file[:2]} {c.title} →</a></div>'
    return '<div class="next"><a href="00-start-here.html">All done. Back to the start ↑</a></div>'


def index(title, chs, made_by=""):
    rows = "".join(f'<li><span class="n">{c.file[:2]}</span><a href="{c.file}.html">{c.title}</a><span class="s">{c.status}</span></li>'
                   for c in chs)
    after = f'<div class="after"><p>These pages are made by <b>{made_by}</b>. Edit the chapter files, then run it again.</p></div>' if made_by else ''
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Noto+Sans:wght@400;600;700&display=swap">
<style>{CSS}{NAVCSS}</style>
</head>
<body>
<main>
<h1>{title}</h1>
<p class="sub">Do them in number order. Drawings are simple sketches, not to scale.</p>
<ol class="toc">{rows}</ol>
{after}
</main>
</body>
</html>'''


def nav_bar(links):
    """A free-standing nav bar for extra pages: links = [(href, label), ...] left to right."""
    return '<div class="nav">' + ''.join(f'<a href="{h}">{t}</a>' for h, t in links) + '</div>'


def with_nav_css(html):
    return html.replace("</style>", NAVCSS + "</style>", 1)


def write_book(out_dir, title, chapters, made_by=""):
    """Write every chapter plus 00-start-here.html into out_dir; returns the paths written."""
    written = []
    for i, c in enumerate(chapters):
        html = with_nav_css(c.module.build(_nav(chapters, i)).replace('</main>', _foot(chapters, i) + '</main>'))
        p = os.path.join(out_dir, c.file + ".html")
        with open(p, "w") as f:
            f.write(html)
        written.append(p)
    p = os.path.join(out_dir, "00-start-here.html")
    with open(p, "w") as f:
        f.write(index(title, chapters, made_by))
    return written + [p]
