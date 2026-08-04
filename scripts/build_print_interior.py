#!/usr/bin/env python3
"""Build a print-ready interior PDF (KDP paperback) from the manuscript.

Usage:
    python3 scripts/build_print_interior.py
    python3 scripts/build_print_interior.py --trim 6x9
    python3 scripts/build_print_interior.py --inside-margin 0.75 --outside-margin 0.5

Default trim is 5.5 x 8.5 inches, a standard commercial fiction size.
Margins default to a conservative KDP-safe gutter; call
`python3 scripts/build_print_interior.py --report-pages` after a first
render to see the actual page count, then tighten --inside-margin to
match KDP's page-count-based minimum if you change trim or font size.

Writes build/the-wife-of-pontius-pilate-print.pdf. Source files are
never modified.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bookcompile import ROOT, FRONT, BACK, chapters, matter_files, parse_matter_blocks, total_words, inline_html  # noqa: E402

BUILD = ROOT / "build"
TITLE = "The Wife of Pontius Pilate"
AUTHOR = "Dustin Ober"
SCENE_BREAK = "•  •  •"

TRIM_PRESETS = {
    "5.5x8.5": (5.5, 8.5),
    "5x8": (5.0, 8.0),
    "6x9": (6.0, 9.0),
}

# Files that get a bare, unheaded, centered treatment (title page, dedication,
# epigraph) rather than the standard matter-page layout.
CENTERED_PAGES = {"00-title-page", "02-dedication", "03-epigraph"}
NO_RUNNING_HEAD_PAGES = {"00-title-page", "01-copyright-page", "02-dedication", "03-epigraph"}


def matter_block_html(text: str) -> str:
    out = []
    for kind, content in parse_matter_blocks(text):
        if kind == "h1":
            out.append(f"<h1>{inline_html(content)}</h1>")
        elif kind == "h2":
            out.append(f"<h2>{inline_html(content)}</h2>")
        elif kind == "h3":
            out.append(f"<h3>{inline_html(content)}</h3>")
        elif kind == "rule":
            out.append(f'<p class="scenebreak">{SCENE_BREAK}</p>')
        elif kind == "quote":
            out.append(f"<blockquote><p>{inline_html(content)}</p></blockquote>")
        else:
            out.append(f'<p class="mp">{inline_html(content)}</p>')
    return "\n".join(out)


def chapter_html(anchor: str, title: str, blocks, *, is_first: bool) -> str:
    page_class = "chapter-open" + ("" if is_first else "")
    parts = [f'<div class="{page_class}" id="{anchor}">', f"<h1>{inline_html(title)}</h1>"]
    first = True
    for kind, text in blocks:
        if kind == "section":
            parts.append(f'<p class="scenebreak">{SCENE_BREAK}</p>')
            first = True
        else:
            cls = "noindent" if first else ""
            parts.append(f'<p class="{cls}">{inline_html(text)}</p>')
            first = False
    parts.append("</div>")
    return "\n".join(parts)


def build_html(args) -> str:
    front_html: list[str] = []
    for path, body in matter_files(FRONT, include_retail_only=True):
        stem = path.stem
        klass = "matter-centered" if stem in CENTERED_PAGES else "matter"
        no_head = "no-running-head" if stem in NO_RUNNING_HEAD_PAGES else ""
        front_html.append(f'<div class="{klass} front-matter page-{stem} {no_head}">')
        front_html.append(matter_block_html(body))
        front_html.append("</div>")

    chapter_list = list(chapters())
    toc_rows = []
    chapter_html_blocks = []
    for idx, (path, title, blocks) in enumerate(chapter_list):
        anchor = f"ch{idx:02d}"
        toc_rows.append(
            f'<li><a class="tocentry" href="#{anchor}">'
            f'<span class="toctitle">{inline_html(title)}</span>'
            f'<span class="leader"></span>'
            f'</a></li>'
        )
        chapter_html_blocks.append(chapter_html(anchor, title, blocks, is_first=(idx == 0)))

    toc_html = f"""
<div class="matter front-matter toc no-running-head">
<h1>Contents</h1>
<ol class="toclist">
{''.join(toc_rows)}
</ol>
</div>
"""

    back_html: list[str] = []
    for path, body in matter_files(BACK, include_retail_only=True):
        back_html.append('<div class="matter back-matter">')
        back_html.append(matter_block_html(body))
        back_html.append("</div>")

    body = "\n".join(front_html) + toc_html + "\n".join(chapter_html_blocks) + "\n".join(back_html)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<title>{TITLE}</title>
<style>{page_css(args)}</style>
</head>
<body>
{body}
</body>
</html>
"""


def page_css(args) -> str:
    w, h = args.trim_w, args.trim_h
    inside, outside, top, bottom = args.inside_margin, args.outside_margin, args.top_margin, args.bottom_margin
    return f"""
@page {{
  size: {w}in {h}in;
  margin-top: {top}in;
  margin-bottom: {bottom}in;
}}
@page :right {{
  margin-left: {inside}in;
  margin-right: {outside}in;
  @top-center {{ content: string(runninghead); font-family: "Liberation Serif", serif; font-size: 8.5pt; font-style: italic; color: #444; }}
  @bottom-center {{ content: counter(page); font-family: "Liberation Serif", serif; font-size: 9pt; }}
}}
@page :left {{
  margin-left: {outside}in;
  margin-right: {inside}in;
  @top-center {{ content: string(bookauthor); font-family: "Liberation Serif", serif; font-size: 8.5pt; font-variant: small-caps; color: #444; }}
  @bottom-center {{ content: counter(page); font-family: "Liberation Serif", serif; font-size: 9pt; }}
}}
@page frontmatter {{
  size: {w}in {h}in;
  margin: {top}in {outside}in {bottom}in {inside}in;
  @top-center {{ content: ""; }}
  @bottom-center {{ content: ""; }}
}}

html {{ hyphens: auto; }}
body {{
  font-family: "Liberation Serif", "DejaVu Serif", serif;
  font-size: {args.font_size}pt;
  line-height: {args.leading};
  color: #111;
}}

.front-matter, .toc {{ page: frontmatter; break-before: page; }}
.front-matter:first-child {{ break-before: avoid; }}
.matter.back-matter {{ break-before: right; }}

h1 {{ string-set: runninghead content(); }}
body {{ string-set: bookauthor "{AUTHOR}"; }}

.chapter-open {{ break-before: right; }}

h1 {{
  font-size: 1.5em;
  font-weight: normal;
  letter-spacing: 0.05em;
  text-align: center;
  margin: 2.4in 0 0.9in 0;
}}
.matter h1, .toc h1 {{ margin: 0.6in 0 0.6in 0; }}
h2 {{
  font-size: 1.05em;
  font-style: italic;
  font-weight: normal;
  text-align: center;
  margin: 1.6em 0 1em 0;
}}

p {{
  margin: 0;
  text-indent: 1.3em;
  text-align: justify;
  orphans: 2;
  widows: 2;
  hyphens: auto;
}}
p.noindent {{ text-indent: 0; }}
p.noindent::first-line {{ font-variant: small-caps; letter-spacing: 0.02em; }}
p.mp {{ text-indent: 0; margin-bottom: 0.7em; text-align: left; }}
p.scenebreak {{
  text-indent: 0;
  text-align: center;
  margin: 1.1em 0;
  letter-spacing: 0.3em;
  hyphens: none;
}}

blockquote {{ margin: 1.4em 10%; }}
blockquote p {{ text-indent: 0; text-align: left; font-style: italic; }}

.matter-centered {{ text-align: center; }}
.matter-centered p.mp {{ text-align: center; text-indent: 0; }}
.matter-centered h1 {{ margin-top: 2.6in; }}
.page-00-title-page {{ margin-top: 2.2in; }}
.page-00-title-page p.mp:first-of-type {{ font-size: 1.3em; letter-spacing: 0.04em; margin-bottom: 0.5em; }}
.page-00-title-page p.mp:nth-of-type(2) {{ margin-bottom: 2.2em; font-style: italic; }}
.page-02-dedication {{ margin-top: 2.8in; }}

.toclist {{ list-style: none; margin: 0; padding: 0; font-size: 0.95em; }}
.toclist li {{ margin: 0.5em 0; }}
.toclist a.tocentry {{ text-decoration: none; color: inherit; display: flex; align-items: baseline; }}
.toclist .leader {{ flex: 1; border-bottom: 1px dotted #999; margin: 0 0.4em 0.15em 0.4em; }}
.toclist a.tocentry::after {{ content: target-counter(attr(href), page); }}
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--trim", default="5.5x8.5", choices=sorted(TRIM_PRESETS))
    ap.add_argument("--inside-margin", type=float, default=0.75, help="binding-side margin, inches")
    ap.add_argument("--outside-margin", type=float, default=0.5, help="outer margin, inches")
    ap.add_argument("--top-margin", type=float, default=0.6, help="inches")
    ap.add_argument("--bottom-margin", type=float, default=0.7, help="inches")
    ap.add_argument("--font-size", type=float, default=11.0, help="points")
    ap.add_argument("--leading", type=float, default=1.42, help="unitless line-height multiplier")
    ap.add_argument("--save-html", action="store_true", help="also write the intermediate HTML for inspection")
    args = ap.parse_args()
    args.trim_w, args.trim_h = TRIM_PRESETS[args.trim]

    html = build_html(args)
    BUILD.mkdir(exist_ok=True)
    if args.save_html:
        (BUILD / "print-interior.html").write_text(html, encoding="utf-8")

    from weasyprint import HTML

    out_path = BUILD / "the-wife-of-pontius-pilate-print.pdf"
    HTML(string=html, base_url=str(ROOT)).write_pdf(out_path)

    import fitz  # PyMuPDF, used only to report the resulting page count

    doc = fitz.open(out_path)
    page_count = doc.page_count
    doc.close()

    print(f"chapters compiled : {len(list(chapters()))}")
    print(f"prose words       : {total_words():,}")
    print(f"trim              : {args.trim_w}in x {args.trim_h}in")
    print(f"margins (in/out)  : {args.inside_margin}in / {args.outside_margin}in")
    print(f"pdf               : {out_path.relative_to(ROOT)}")
    print(f"page count        : {page_count}")
    if page_count % 2 != 0:
        print("note              : odd total page count; KDP pads to even automatically, or add a blank back-matter page")


if __name__ == "__main__":
    main()
