#!/usr/bin/env python3
"""Build a valid EPUB3 ebook from the manuscript and retail matter.

Usage:
    python3 scripts/build_epub.py
    python3 scripts/build_epub.py --cover path/to/cover.jpg
    python3 scripts/build_epub.py --keep-section-titles

Writes build/the-wife-of-pontius-pilate.epub. Source files are never
modified. The .epub does not embed a cover image unless --cover is
passed: Amazon KDP accepts the cover as a separate upload, but Apple
Books, Kobo, and most aggregators require it embedded, so pass --cover
once final cover art exists.
"""

from __future__ import annotations

import argparse
import datetime
import re
import sys
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from bookcompile import (  # noqa: E402
    ROOT, FRONT, BACK, chapters, matter_files, parse_matter_blocks, total_words, esc, inline_html,
)

BUILD = ROOT / "build"
TITLE = "The Wife of Pontius Pilate"
AUTHOR = "Dustin Ober"
LANG = "en"

# Generated once with uuid.uuid4() and fixed here so re-running the build
# does not mint a new identifier every time. Replace with a urn:isbn: form
# if an ISBN is assigned to the ebook edition.
BOOK_UUID = "031a9100-7d66-47e9-93c8-244db4a7ea46"

SCENE_BREAK = "• • •"  # bullet  em-space  bullet  em-space  bullet


inline_xhtml = inline_html  # local alias kept for readability in this file


def xhtml_page(title: str, body_html: str, *, epub_type: str = "bodymatter") -> str:
    return f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">
<head>
<meta charset="utf-8"/>
<title>{esc(title)}</title>
<link rel="stylesheet" type="text/css" href="../css/style.css"/>
</head>
<body epub:type="{epub_type}">
{body_html}
</body>
</html>
"""


def chapter_xhtml(title: str, blocks, epub_type: str) -> str:
    parts = [f'<section epub:type="{epub_type}">', f"<h1>{esc(title)}</h1>"]
    first = True
    for kind, text in blocks:
        if kind == "section":
            parts.append(f'<p class="scenebreak">{SCENE_BREAK}</p>')
            first = True
        else:
            cls = ' class="noindent"' if first else ""
            parts.append(f"<p{cls}>{inline_xhtml(text)}</p>")
            first = False
    parts.append("</section>")
    return xhtml_page(title, "\n".join(parts), epub_type="chapter" if epub_type == "chapter" else epub_type)


def label_from_stem(stem: str) -> str:
    """Fallback <title> label for a matter page with no '# Heading' of its own."""
    parts = stem.split("-")
    if parts and parts[0].isdigit():
        parts = parts[1:]
    return " ".join(w.capitalize() for w in parts) if parts else stem


def matter_xhtml(heading: str, text: str, epub_type: str, *, page_title: str) -> str:
    parts = [f'<section epub:type="{epub_type}">']
    if heading:
        parts.append(f"<h1>{esc(heading)}</h1>")
    for kind, content in parse_matter_blocks(text):
        if kind == "h1":
            parts.append(f"<h1>{inline_xhtml(content)}</h1>")
        elif kind == "h2":
            parts.append(f"<h2>{inline_xhtml(content)}</h2>")
        elif kind == "h3":
            parts.append(f"<h3>{inline_xhtml(content)}</h3>")
        elif kind == "rule":
            parts.append(f'<p class="scenebreak">{SCENE_BREAK}</p>')
        elif kind == "quote":
            parts.append(f"<blockquote><p>{inline_xhtml(content)}</p></blockquote>")
        else:
            parts.append(f"<p>{inline_xhtml(content)}</p>")
    parts.append("</section>")
    return xhtml_page(page_title, "\n".join(parts), epub_type=epub_type)


MATTER_EPUB_TYPE = {
    "00-title-page": "titlepage",
    "01-copyright-page": "copyright-page",
    "02-dedication": "dedication",
    "03-epigraph": "epigraph",
    "04-dramatis-personae": "loi",
    "01-authors-note": "afterword",
    "02-discussion-questions": "other-credits",
    "03-acknowledgments": "acknowledgments",
    "04-about-the-author": "bio",
    "05-a-request": "other-credits",
}

CSS = """
@namespace epub "http://www.idpf.org/2007/ops";
body { font-family: Georgia, "Liberation Serif", "DejaVu Serif", serif; line-height: 1.5; margin: 0 5%; }
h1 { font-size: 1.4em; text-align: center; margin: 2em 0 1.2em 0; font-weight: normal; letter-spacing: 0.04em; }
h2 { font-size: 1.05em; text-align: center; margin: 1.6em 0 1em 0; font-style: italic; font-weight: normal; }
p { margin: 0; text-indent: 1.3em; text-align: justify; orphans: 2; widows: 2; }
p.noindent { text-indent: 0; }
p.scenebreak { text-indent: 0; text-align: center; margin: 1.2em 0; letter-spacing: 0.2em; }
blockquote { margin: 1.5em 8%; font-style: italic; }
blockquote p { text-indent: 0; text-align: left; }
section[epub|type~="titlepage"] h1 { font-size: 1.9em; margin-top: 30%; }
section[epub|type~="titlepage"] p { text-indent: 0; text-align: center; font-style: italic; }
section[epub|type~="copyright-page"] p, section[epub|type~="dedication"] p,
section[epub|type~="acknowledgments"] p, section[epub|type~="bio"] p { text-indent: 0; text-align: left; font-size: 0.9em; }
section[epub|type~="dedication"] p { text-align: center; font-style: italic; margin-top: 35%; }
section[epub|type~="epigraph"] { margin-top: 30%; }
section[epub|type~="epigraph"] blockquote p { text-align: center; font-style: italic; }
"""


def build(args) -> Path:
    front_files = list(matter_files(FRONT, include_retail_only=True))
    back_files = list(matter_files(BACK, include_retail_only=True))
    chapter_list = list(chapters())

    manifest_items: list[tuple[str, str, str]] = []  # (id, href, media-type)
    spine_ids: list[str] = []
    nav_entries: list[tuple[str, str]] = []  # (href, label) for chapters only
    text_files: dict[str, str] = {}

    def register(item_id: str, href: str, media_type: str, *, in_spine: bool = True):
        manifest_items.append((item_id, href, media_type))
        if in_spine:
            spine_ids.append(item_id)

    for path, body in front_files:
        stem = path.stem
        item_id = f"front-{stem}"  # XML NCName: item ids may not start with a digit
        etype = MATTER_EPUB_TYPE.get(stem, "frontmatter")
        blocks = parse_matter_blocks(body)
        heading = next((t for k, t in blocks if k == "h1"), "")
        href = f"text/{stem}.xhtml"
        text_files[href] = matter_xhtml(
            heading if stem != "00-title-page" else "",
            body, etype, page_title=heading or label_from_stem(stem),
        )
        register(item_id, href, "application/xhtml+xml")

    for idx, (path, title, blocks) in enumerate(chapter_list):
        etype = "prologue" if idx == 0 else ("epilogue" if idx == len(chapter_list) - 1 else "chapter")
        item_id = f"ch{idx:02d}"
        href = f"text/{item_id}.xhtml"
        text_files[href] = chapter_xhtml(title, blocks, etype)
        register(item_id, href, "application/xhtml+xml")
        nav_entries.append((href, title))

    for path, body in back_files:
        stem = path.stem
        item_id = f"back-{stem}"
        etype = MATTER_EPUB_TYPE.get(stem, "backmatter")
        blocks = parse_matter_blocks(body)
        heading = next((t for k, t in blocks if k == "h1"), "")
        href = f"text/{stem}.xhtml"
        text_files[href] = matter_xhtml(heading, body, etype, page_title=heading or label_from_stem(stem))
        register(item_id, href, "application/xhtml+xml")

    cover_href = None
    if args.cover:
        cover_path = Path(args.cover)
        ext = cover_path.suffix.lower().lstrip(".")
        media = {"jpg": "image/jpeg", "jpeg": "image/jpeg", "png": "image/png"}.get(ext)
        if not media:
            raise SystemExit(f"unsupported cover image type: {cover_path.suffix}")
        cover_href = f"images/cover.{ext}"
        manifest_items.insert(0, ("cover-image", cover_href, media))

    nav_items = "\n".join(f'<li><a href="{href}">{esc(t)}</a></li>' for href, t in nav_entries)
    landmarks = []
    if any(p.stem == "00-title-page" for p, _ in front_files):
        landmarks.append('<li><a epub:type="titlepage" href="text/00-title-page.xhtml">Title Page</a></li>')
    landmarks.append(f'<li><a epub:type="bodymatter" href="{nav_entries[0][0]}">Start of Book</a></li>')
    nav_xhtml = f"""<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="{LANG}">
<head><meta charset="utf-8"/><title>Contents</title><link rel="stylesheet" type="text/css" href="css/style.css"/></head>
<body>
<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>
{nav_items}
</ol></nav>
<nav epub:type="landmarks" hidden="">
<ol>
{''.join(landmarks)}
</ol>
</nav>
</body>
</html>
"""
    register("nav", "nav.xhtml", "application/xhtml+xml", in_spine=False)

    ncx_points = "\n".join(
        f'<navPoint id="np{i}" playOrder="{i+1}"><navLabel><text>{esc(t)}</text></navLabel>'
        f'<content src="{href}"/></navPoint>'
        for i, (href, t) in enumerate(nav_entries)
    )
    toc_ncx = f"""<?xml version="1.0" encoding="utf-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
<head>
<meta name="dtb:uid" content="urn:uuid:{BOOK_UUID}"/>
<meta name="dtb:depth" content="1"/>
<meta name="dtb:totalPageCount" content="0"/>
<meta name="dtb:maxPageNumber" content="0"/>
</head>
<docTitle><text>{esc(TITLE)}</text></docTitle>
<navMap>
{ncx_points}
</navMap>
</ncx>
"""
    register("ncx", "toc.ncx", "application/x-dtbncx+xml", in_spine=False)
    register("css", "css/style.css", "text/css", in_spine=False)

    today = datetime.date.today().isoformat() if not args.fixed_date else "2026-01-01"
    def manifest_item(iid: str, href: str, mt: str) -> str:
        props = ""
        if iid == "nav":
            props = ' properties="nav"'
        elif iid == "cover-image":
            props = ' properties="cover-image"'
        return f'<item id="{iid}" href="{href}" media-type="{mt}"{props}/>'

    manifest_xml = "\n".join(manifest_item(iid, href, mt) for iid, href, mt in manifest_items)
    spine_xml = "\n".join(f'<itemref idref="{iid}"/>' for iid in spine_ids)
    meta_cover = f'<meta name="cover" content="cover-image"/>' if cover_href else ""

    content_opf = f"""<?xml version="1.0" encoding="utf-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bookid" xml:lang="{LANG}">
<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
<dc:identifier id="bookid">urn:uuid:{BOOK_UUID}</dc:identifier>
<dc:title>{esc(TITLE)}</dc:title>
<dc:creator id="creator">{esc(AUTHOR)}</dc:creator>
<meta refines="#creator" property="role" scheme="marc:relators">aut</meta>
<dc:language>{LANG}</dc:language>
<dc:date>{today}</dc:date>
<dc:rights>Copyright (c) {datetime.date.today().year} {esc(AUTHOR)}. All rights reserved.</dc:rights>
<meta property="dcterms:modified">{datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ') if not args.fixed_date else '2026-01-01T00:00:00Z'}</meta>
{meta_cover}
</metadata>
<manifest>
{manifest_xml}
</manifest>
<spine toc="ncx">
{spine_xml}
</spine>
</package>
"""

    BUILD.mkdir(exist_ok=True)
    out_path = BUILD / "the-wife-of-pontius-pilate.epub"
    if out_path.exists():
        out_path.unlink()

    with zipfile.ZipFile(out_path, "w") as zf:
        zf.writestr("mimetype", "application/epub+zip", compress_type=zipfile.ZIP_STORED)
        zf.writestr(
            "META-INF/container.xml",
            """<?xml version="1.0" encoding="UTF-8"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
<rootfiles><rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/></rootfiles>
</container>
""",
        )
        zf.writestr("OEBPS/content.opf", content_opf)
        zf.writestr("OEBPS/nav.xhtml", nav_xhtml)
        zf.writestr("OEBPS/toc.ncx", toc_ncx)
        zf.writestr("OEBPS/css/style.css", CSS)
        for href, xhtml in text_files.items():
            zf.writestr(f"OEBPS/{href}", xhtml)
        if cover_href:
            zf.writestr(f"OEBPS/{cover_href}", Path(args.cover).read_bytes())

    return out_path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cover", help="path to a JPG/PNG cover image to embed")
    ap.add_argument("--keep-section-titles", action="store_true", help="unused, kept for CLI symmetry")
    ap.add_argument("--fixed-date", action="store_true", help="use a fixed date so rebuilds are byte-stable (for diffing)")
    args = ap.parse_args()

    out_path = build(args)
    print(f"chapters compiled : {len(list(chapters()))}")
    print(f"prose words       : {total_words():,}")
    print(f"epub              : {out_path.relative_to(ROOT)}")
    if not args.cover:
        print("cover             : NOT embedded (pass --cover once final art exists)")


if __name__ == "__main__":
    main()
