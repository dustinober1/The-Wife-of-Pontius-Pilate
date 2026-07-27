#!/usr/bin/env python3
"""Count drafted manuscript prose while excluding outline-only stubs and Markdown metadata.

Usage:
    python scripts/word_count.py
    python scripts/word_count.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

MANUSCRIPT_DIR = Path(__file__).resolve().parents[1] / "manuscript"
STUB_MARKER = "Status: outline only"
WORD_RE = re.compile(r"\b[\w’'-]+\b", re.UNICODE)


def is_drafted(text: str) -> bool:
    return STUB_MARKER not in text


def prose_text(text: str) -> str:
    lines: list[str] = []
    in_fence = False
    for raw in text.splitlines():
        line = raw.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or not line:
            continue
        if line.startswith("#"):
            continue
        if line.startswith(">"):
            continue
        if re.fullmatch(r"\*[^*]+\*", line):
            continue
        lines.append(raw)
    return "\n".join(lines)


def count_words(text: str) -> int:
    return len(WORD_RE.findall(prose_text(text)))


def collect() -> tuple[list[dict[str, object]], int]:
    rows: list[dict[str, object]] = []
    total = 0
    for path in sorted(MANUSCRIPT_DIR.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        drafted = is_drafted(text)
        words = count_words(text) if drafted else 0
        rows.append({"file": path.relative_to(MANUSCRIPT_DIR.parent).as_posix(), "drafted": drafted, "words": words})
        total += words
    return rows, total


def main() -> None:
    if os.environ.get("GITHUB_ACTIONS") == "true":
        from batch01_capture import capture

        capture(count_words=count_words, is_drafted=is_drafted)

    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    rows, total = collect()
    if args.json:
        print(json.dumps({"files": rows, "total_drafted_words": total}, indent=2))
        return
    for row in rows:
        state = "DRAFT" if row["drafted"] else "STUB "
        print(f"{state} {row['words']:6d}  {row['file']}")
    print(f"TOTAL DRAFTED PROSE: {total}")


if __name__ == "__main__":
    main()
