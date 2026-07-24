# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

This is not a software project — it's the manuscript repo for a historical novel, *The Wife of Pontius Pilate*. There is no build, lint, or test tooling; all work here is drafting and revising prose in Markdown. "Development" means writing chapters, keeping them consistent with the outline, and maintaining continuity threads across the book.

## Repository structure

- `OUTLINE.md` — the master plan: full chapter list, POV assignments, target word counts, part-by-part beat summaries, the recurring continuity threads, and the suggested drafting order. Treat this as the source of truth for structure. If a chapter's content changes meaningfully during drafting, update the corresponding row in `OUTLINE.md` to match.
- `CHARACTERS.md` — the cast sheet: ages, appearances, voices, and status for every recurring figure, plus the "locked continuity facts" already fixed by drafted prose. Facts marked **(on page)** cannot be contradicted; when a new chapter locks a new fact (a name, an age, a physical detail), promote it into this file.
- `TIMELINE.md` — the historical spine (dated events with primary sources) and the book-internal chronology (invented events with derived dates). Check both before drafting any chapter; keep the aqueduct-riot placement (~A.D. 28–29) consistent everywhere.
- `STYLE.md` — prose conventions derived from the drafted chapters: POV mechanics, anachronism policy, naming rules ("Pontius" never "Pilate" in narration), dialogue punctuation, and thread discipline. Follow it when drafting; update it only when a deliberate style decision changes.
- `manuscript/` — one file per chapter, including the Prologue and Epilogue.

### Manuscript file naming

Files are numbered in reading order, zero-padded two digits, followed by a slug of the title:

```
manuscript/00-prologue-the-shadow-of-the-bema.md
manuscript/01-the-red-seal.md
manuscript/02-the-roman-bride.md
...
manuscript/29-the-recall.md
manuscript/30-epilogue-the-far-shore.md
```

The Prologue is `00`, chapters 1–29 map directly to their chapter number, and the Epilogue is `30`. When drafting a not-yet-written chapter, edit the existing stub file in place — don't create a second file for the same chapter.

### Drafted chapter format

Chapters with finished prose (currently the Prologue, Chapter 1, and Chapter 2) use this shape:

```markdown
# Chapter N: Title

## Scene/Section Heading

Prose...

## Next Scene/Section Heading

Prose...
```

Section headings (`##`) break each chapter into its named scenes/beats (e.g., "The Waking Nightmare," "The View from the Balcony"). Follow this pattern when drafting new chapters — use the scene beats already named in `OUTLINE.md`'s "Key Beats" column as a starting point for section structure where it makes sense.

### Undrafted chapter (stub) format

Chapters not yet written use a metadata stub, e.g. `manuscript/03-landfall.md`:

```markdown
# Chapter 3: Landfall

*POV: Claudia*
*Setting: Caesarea Maritima*
*Target length: ~2,900*

> **Status: outline only — not yet drafted.**
>
> Key beats: First sight of Judaea; Herod's old palace as praetorium; introduce Tamar...
```

The `*Setting: ...*` line only appears when `OUTLINE.md` specifies a Time/Place for that chapter (Part I chapters have it; later parts generally don't). When a stub is drafted into full prose, remove the metadata block and status blockquote entirely — replace it with the chapter's actual scenes, matching the drafted-chapter format above.

## Story bible (keep every chapter consistent with this)

- **POV**: Close third person throughout. Claudia is the default POV; Pontius gets POV chapters only at the specific turning points marked in `OUTLINE.md` (currently chapters 4, 6, 9, 15, 16, 19, 25, 28).
- **Faith arc**: Claudia's eventual turn toward belief must read as earned through conscience, grief, and doubt — never as a doctrinal or overtly supernatural conversion scene. It should be legible as either religious faith or moral awakening; the prose should not force one reading over the other.
- **Recurring threads** — these must be deliberately seeded and paid off across the book, not just in the chapters that introduce them:
  - **Water / the fractured reflection**: fountain (Ch1) → black water at Ostia (Ch1) → a basin at the trial → final image in the Epilogue.
  - **Ink-stained hands**: Claudia's childhood lesson that she's loved for being useful (Ch2) → the warning note to Pontius (Prologue) → one late, conscious callback near the end.
  - **The map**: "you have not mapped their pride" (Ch1) → a second map scene after Sejanus falls → no map at all by the Epilogue.
  - **Marcus**: secretary/steward, present at nearly every major public moment; his small reactions are how the reader sees Claudia's conscience forming, without narration stating it outright.
  - **The dream**: must be seeded twice, lightly, before Part IV (Ch14 "The Dream Begins," Ch20 "The Second Dream"), so its full arrival in the Prologue doesn't feel unearned.
- **Structural note**: Chapters 22–23 rejoin the Prologue's beats (the waking dream, the balcony view, the message to Pontius, the locked gaze) in freshly written prose rather than repeating its text verbatim. An earlier draft had Ch22's ending and Ch23's opening reproduce the Prologue almost word for word; an external editorial review flagged that this much exact repetition stalled the climax for a reader returning to it twenty-plus chapters later, so it was trimmed to a rhyme — same images, same sequence of events, same key phrases (the ink-stained thumb, the forty yards, the bronze clasp) — without restating whole paragraphs. When revising either chapter, cross-check `manuscript/00-prologue-the-shadow-of-the-bema.md` for continuity of action and imagery, not for matching sentences.

## Prose style constraints

These apply to every chapter, drafted or in revision — they are the most common tells of AI-generated prose and must be actively avoided, not just left unfixed when noticed:

- **No em dashes.** Rewrite the sentence with a period, comma, colon, or parenthetical instead. This includes the em dash used as a dramatic pause before a final clause.
- **No "not X, but Y" (or "not quite X, but Y") constructions**, and no other negative-parallelism hedges ("not merely...", "less an X than a Y", "if not X, then at least Y"). State what the thing is, directly, rather than defining it by what it isn't.
- Be alert generally to other signs of AI writing when drafting or revising: rule-of-three lists, inflated symbolism stated outright rather than left implicit, vague attributions ("some say," "many believe"), excessive conjunctive throat-clearing ("Moreover," "Furthermore," "That said"), and summarizing a scene's meaning in the narration instead of trusting the reader. When in doubt, run a pass with the `humanizer` skill before considering a chapter finished.

## Word counts

Target lengths are per-chapter in `OUTLINE.md` and in each stub's `*Target length*` line; there's a running total at the bottom of `OUTLINE.md` (drafted vs. new material vs. projected finished length ~81,300–85,000 words). To check current word counts:

```bash
wc -w manuscript/*.md
```

## Suggested drafting order

Per `OUTLINE.md`: draft in chapter order, since the historical hinge points (Ch 6, 16, 23, 28) land better when the chapters that set them up are freshly written. The eight Pontius-POV chapters (4, 6, 9, 15, 16, 19, 25, 28) share a throughline — a man whose theory of rule ("an even hand and an unbending spine") is tested and eroded one crisis at a time — and can be drafted as a mini-arc on their own if a change of pace is wanted, then interleaved back into order.
