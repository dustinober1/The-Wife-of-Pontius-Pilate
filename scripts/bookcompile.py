"""Shared manuscript-compilation helpers for the build scripts.

Parses manuscript/*.md into (title, blocks) and provides ordered access
to the retail front-matter/ and back-matter/ folders. Nothing here writes
to manuscript/, front-matter/, or back-matter/.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript"
FRONT = ROOT / "front-matter"
BACK = ROOT / "back-matter"

POV_RE = re.compile(r"^\*POV:[^*]*\*$")
RETAIL_ONLY_MARKER = "<!-- retail-only -->"


def parse_chapter(path: Path):
    """Return (title, blocks). Each block is ('section'|'para', text)."""
    title = None
    blocks: list[tuple[str, str]] = []
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("# "):
            title = line[2:].strip()
            continue
        if POV_RE.fullmatch(line):
            continue
        if line.startswith("## "):
            blocks.append(("section", line[3:].strip()))
            continue
        blocks.append(("para", line))
    return title, blocks


def chapters():
    for path in sorted(MANUSCRIPT.glob("*.md")):
        title, blocks = parse_chapter(path)
        yield path, title, blocks


def matter_files(folder: Path, *, include_retail_only: bool = True):
    """Yield markdown matter files in filename order.

    Files opening with RETAIL_ONLY_MARKER are skipped when
    include_retail_only is False (used by the agent-submission build,
    which must not carry copyright pages, dedications, or back-cover
    apparatus into a query manuscript).
    """
    for path in sorted(folder.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        is_retail_only = text.lstrip().startswith(RETAIL_ONLY_MARKER)
        if is_retail_only and not include_retail_only:
            continue
        body = text.replace(RETAIL_ONLY_MARKER, "", 1).strip("\n")
        yield path, body


def parse_matter_blocks(text: str):
    """Parse a front/back-matter markdown file into simple render blocks.

    Recognises: h1 (#), h2 (##), horizontal rule (---), blockquote (>),
    and paragraphs. Bold **like this** and italic *like this* are left
    inline for the renderer to interpret.
    """
    blocks: list[tuple[str, str]] = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line == "---":
            blocks.append(("rule", ""))
        elif line.startswith("### "):
            blocks.append(("h3", line[4:].strip()))
        elif line.startswith("## "):
            blocks.append(("h2", line[3:].strip()))
        elif line.startswith("# "):
            blocks.append(("h1", line[2:].strip()))
        elif line.startswith(">"):
            blocks.append(("quote", line.lstrip(">").strip()))
        else:
            blocks.append(("para", line))
    return blocks


def esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline_html(text: str) -> str:
    """Render **bold** and *italic* markdown spans as escaped (X)HTML."""
    out: list[str] = []
    for part in re.split(r"(\*\*[^*]+\*\*)", text):
        if part.startswith("**") and part.endswith("**"):
            out.append(f"<strong>{esc(part[2:-2])}</strong>")
        else:
            for sp in re.split(r"(\*[^*]+\*)", part):
                if sp.startswith("*") and sp.endswith("*") and len(sp) > 1:
                    out.append(f"<em>{esc(sp[1:-1])}</em>")
                else:
                    out.append(esc(sp))
    return "".join(out)


WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)


def total_words() -> int:
    total = 0
    for _, _, blocks in chapters():
        total += len(WORD_RE.findall(" ".join(t for k, t in blocks if k == "para")))
    return total
