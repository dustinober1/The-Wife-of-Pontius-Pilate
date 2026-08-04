# Self-Publishing Readiness Report

## Status

The book has three retail-ready deliverables, both independently
validated: an EPUB that passes official EPUBCheck with zero errors, and a
print-ready interior PDF with book-grade typesetting (running heads,
folios, an auto-paginating table of contents, chapter openings starting
on recto pages, small-caps chapter-opening lines). The agent-submission
`.docx`/`.md` pair from the prior pass still builds and is unaffected.

This supersedes the agent-route work from the previous session. The
query letter and synopsis in `submission/` are left in place, since they
cost nothing to keep and might matter later (foreign rights, audio,
changing your mind), but they are not the active path.

## What changed structurally

Front and back matter were reorganized from a submission packet into a
retail book's actual front and back matter, in reading order:

**Front matter:** title page, copyright page, dedication, epigraph
(Matthew 27:19, KJV), cast of characters. **Back matter:** author's note
(carried over from the last pass), discussion questions, acknowledgments,
about the author, a request for reviews.

A `<!-- retail-only -->` marker at the top of a matter file excludes it
from the agent-format build, so `scripts/build_manuscript.py` (unchanged
in purpose) still produces a clean submission manuscript: title page,
epigraph, cast list, the text, author's note. No copyright page, no
dedication, no discussion questions leak into that file.

A shared module, `scripts/bookcompile.py`, now holds the chapter parser
and the front/back-matter loader so all three build scripts (agent
`.docx`, EPUB, print PDF) read the exact same source content and cannot
drift from one another. All three report the same word count, 80,847,
independently.

## The three build scripts

```bash
python3 scripts/build_manuscript.py        # agent-format .docx and .md (unchanged path)
python3 scripts/build_epub.py               # retail EPUB3
python3 scripts/build_epub.py --cover cover.jpg   # same, with a cover image embedded
python3 scripts/build_print_interior.py     # print-ready interior PDF, 5.5x8.5in default
python3 scripts/build_print_interior.py --trim 6x9 --inside-margin 0.75
```

None of the three ever writes to `manuscript/`, `front-matter/`, or
`back-matter/`.

### EPUB

Hand-built as a valid EPUB3 package (no external library), because the
available EPUB-generation packages could not be installed in this
environment and the manual approach gives full control over the
structural-semantics vocabulary (`epub:type="chapter"`, `"prologue"`,
`"epilogue"`, `"titlepage"`, `"copyright-page"`, `"dedication"`,
`"epigraph"`) that accessible-reading-order tools use.

Validated with the official EPUBCheck 5.1.0 (fetched and run against the
build, not just structurally sanity-checked by hand): **zero errors, zero
warnings.** Three real defects were caught and fixed by that run, not by
inspection: manifest item IDs derived from filenames like `00-title-page`
are invalid XML names (an XML Name cannot start with a digit), the
`<spine>` element was missing its required `toc` attribute once an NCX
was included for backward compatibility, and the stylesheet was written
into the package but never declared in the manifest, which every
XHTML file referenced but no reading system could resolve.

The EPUB does not embed a cover image, since none exists yet. `--cover`
adds one when you have final art; Amazon KDP accepts the cover as a
separate upload regardless, but Apple Books, Kobo, and most aggregators
require it embedded in the file itself, so pass the flag before
distributing anywhere but Amazon.

### Print interior PDF

Built with WeasyPrint from generated HTML and CSS, which gives real
control over paginated typesetting that a fixed export format cannot
(alternating running heads, a table of contents whose page numbers
resolve automatically via CSS `target-counter()`, chapters forced to
start on a recto page).

Two real defects surfaced only by rendering actual pages to images and
looking at them, not by any automated check:

- A CSS `page` property set on the whole chapter container was inherited
  by every page that chapter's content flowed onto, not just its first
  page. The intended effect (no running head on a chapter's opening page)
  instead suppressed the running head for the chapter's *entire* length.
  Fixed by dropping the named-page mechanism for chapter openers in favor
  of uniform running heads on every body page, which is itself a common
  and entirely acceptable convention in commercial fiction, not a
  compromise.
- The title page had no vertical placement logic and rendered flush to
  the top margin. Added explicit positioning so the title, subtitle, and
  author name fall roughly a third of the way down the page, matching
  ordinary trade-paperback convention.

The table of contents' auto-numbering also failed silently on the first
attempt: `target-counter(attr(href url), page)` used CSS's typed-attr
syntax, which WeasyPrint does not parse, and the declaration was simply
dropped with no error. Confirmed against an isolated test case that plain
`attr(href)` works, then found a second, separate bug in the same
feature: the generated-content rule was on a `<span>` sibling of the
`<a>` rather than on the anchor itself, so `attr(href)` had nothing to
read. Both are fixed; the contents page now resolves real page numbers
for all 31 chapters in a single render pass.

Every fix above was verified against an actual rendered page, not just
against the generating code: pages were rasterized with PyMuPDF and
inspected directly, the way a reader would see them.

**Current output:** 5.5in x 8.5in trim (a standard commercial fiction
size), 383 pages, Liberation Serif body text at 11pt, justified with
hyphenation, alternating running heads (chapter title on recto pages,
author name in small caps on verso pages, both driven by CSS `string-set`
so they update automatically as chapters change), folios at bottom
center, chapters starting on recto pages, small-caps treatment on
chapter- and section-opening lines, a widow/orphan-controlled layout, and
an auto-paginating contents page.

**This page count will move** once the dedication, acknowledgments, and
about-the-author placeholders are replaced with real text, and again if
you change trim size, font size, or margins. Rerun the script and check
the reported count before finalizing a wraparound cover, which needs an
exact page count to set spine width.

## New assets

| Path | Purpose |
|---|---|
| `front-matter/01-copyright-page.md` | Copyright notice, fiction disclaimer, ISBN/cover-credit placeholders |
| `front-matter/02-dedication.md` | Placeholder, personal |
| `front-matter/03-epigraph.md` | Matthew 27:19, KJV (public domain) |
| `back-matter/02-discussion-questions.md` | 15 reading-group questions grounded in the text |
| `back-matter/03-acknowledgments.md` | Placeholder, personal |
| `back-matter/04-about-the-author.md` | Placeholder template |
| `back-matter/05-a-request.md` | Short, universal review-request page |
| `scripts/bookcompile.py` | Shared chapter/matter-file parser used by all three builders |
| `scripts/build_epub.py` | EPUB3 builder |
| `scripts/build_print_interior.py` | Print-interior PDF builder |
| `retail/kdp-metadata.md` | Back-cover copy, categories, keywords, content notes, trim/ISBN/pricing orientation |
| `retail/cover-brief.md` | Cover design brief grounded in the novel's own recurring imagery |
| `build/the-wife-of-pontius-pilate.epub` | Committed deliverable |
| `build/the-wife-of-pontius-pilate-print.pdf` | Committed deliverable |

## Placeholders that must be filled before you publish

Everything below currently renders visibly in both the EPUB and the print
PDF as literal bracketed text. None of it can be written on your behalf;
all of it is personal.

- `front-matter/01-copyright-page.md`: ISBN, cover designer credit, website
- `front-matter/02-dedication.md`
- `back-matter/03-acknowledgments.md`
- `back-matter/04-about-the-author.md`

Rerun all three build scripts after editing any of these.

## Open decisions

1. **Cover art.** Nothing exists. `retail/cover-brief.md` is written for
   either a hired designer or a DIY tool; grounded in the book's actual
   recurring imagery (water, ink-stained hands, a map, the empty judgment
   seat) rather than generic toga-and-column stock art.
2. **Trim size.** Default is 5.5in x 8.5in. `--trim 6x9` or `--trim 5x8`
   are available; 6x9 would run meaningfully fewer, wider pages for the
   same word count.
3. **ISBN.** KDP will assign a free one if you publish exclusively there
   and are fine with it listed as publisher of record. Buy your own via
   Bowker (US) or your national agency if you want wider distribution or
   your own name as publisher. Guidance only in `retail/kdp-metadata.md`;
   no number has been fabricated anywhere in the repo.
4. **Pricing and categories.** Oriented, not prescribed, in
   `retail/kdp-metadata.md`, since both are business decisions and Amazon's
   exact category tree changes over time.

## Not done, and why

**No professional human proofread.** The prior pass corrected mechanical
errors (chapter self-references, time-arithmetic contradictions, a
character-name collision) and this pass corrected structural and
typesetting defects. Neither substitutes for a proofreader reading the
finished, typeset book end to end before it goes live; that is the one
step left between this repository and an actual publish button.

**No line-by-line stylistic rewrite.** As before: the prose voice is the
author's and was not altered beyond the specific corrections logged in
the prior report.

**No real cover art**, for the reason above: it requires either a design
tool or a designer, not text generation.
