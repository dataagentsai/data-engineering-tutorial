"""Build the Data Engineering Tutorial into site/*.html.

    python3 build.py

Same shell as agent-harness-tutorial: pages register with @page(...) in pages_*.py, and the tree of parents
gives the left panel, the breadcrumb, the tabs and the back/next order.
"""
import re
from html import escape
from pathlib import Path

import kit
from reg import PAGES, page, href, link  # noqa: F401

OUT = Path(__file__).parent / "site"
SITE_HOME = "https://cleandataengineering.ai/"
TABS = [("index", "Start"), ("glossary", "Words"), ("dac", "Must be true"), ("dpc", "Must exist"),
        ("slice1", "Slice 1")]


def children(pid):
    return sorted((p for p in PAGES.values() if p["parent"] == pid), key=lambda p: p["order"])


def ancestors(pid):
    out = []
    while pid:
        out.append(pid)
        pid = PAGES[pid]["parent"]
    return out[::-1]


def walk(pid=None):
    for c in children(pid):
        yield c["id"]
        yield from walk(c["id"])


def side(cur):
    items = "".join(f'<li><a class="{"on" if p == cur else ""}" href="{href(p)}">{PAGES[p]["short"]}</a></li>'
                    for p in walk())
    return f"<h4>Data Engineering</h4><ul>{items}</ul>"


def tabs(cur):
    hit = next((a for a in reversed(ancestors(cur)) if a in dict(TABS)), None)
    return "".join(f'<a class="{"on" if t == hit else ""}" href="{href(t)}">{n}</a>' for t, n in TABS)


def pn(cur, order):
    i, s = order.index(cur), ""
    if i > 0:
        p = PAGES[order[i - 1]]
        s += f'<a class="pv" href="{href(p["id"])}"><small>← Back</small>{p["short"]}</a>'
    if i < len(order) - 1:
        n = PAGES[order[i + 1]]
        s += f'<a class="nx" href="{href(n["id"])}"><small>Next →</small>{n["short"]}</a>'
    return f'<nav class="pn">{s}</nav>'


def render(pid, order):
    p = PAGES[pid]
    chain = ancestors(pid)
    crumbs = " › ".join([f'<a href="{href(a)}">{PAGES[a]["short"]}</a>' for a in chain[:-1]] + [f'<b>{p["short"]}</b>'])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{escape(re.sub('<[^>]+>', '', p['short']))} · Data Engineering Tutorial</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Patrick+Hand&family=JetBrains+Mono:wght@500;700&display=swap">
<link rel="stylesheet" href="style.css"></head><body>
{kit.DEFS}
<header class="top"><div class="row"><button class="menu" aria-label="Show the page list">☰ Pages</button>
<a class="home" href="{SITE_HOME}">cleandataengineering.ai</a><a class="brand" href="index.html">Data Engineering, drawn simply</a><nav class="tabs" aria-label="Sections">{tabs(pid)}</nav></div>
<div class="crumbs">You are here: {crumbs}</div></header>
<aside class="side" aria-label="All pages">{side(pid)}</aside>
<main><div class="wrap"><article class="page">
<header><p class="kicker">Data Engineering Tutorial</p><h1>{p['title']}</h1></header>
{p['render']()}
</article>{pn(pid, order)}</div></main>
<script src="nav.js"></script></body></html>"""


def main():
    import pages_start, pages_specs  # noqa: F401
    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("*.html"):
        old.unlink()
    order = list(walk())
    (OUT / "style.css").write_text(kit.CSS)
    (OUT / "nav.js").write_text(kit.JS)
    for pid in order:
        (OUT / href(pid)).write_text(render(pid, order))
    bad = [(f.name, h) for f in OUT.glob("*.html") for h in re.findall(r'href="([a-z0-9-]+)\.html"', f.read_text())
           if h not in PAGES]
    assert not bad, bad
    print(f"{len(order)} pages -> {OUT}")


if __name__ == "__main__":
    main()
