# Publication Readiness Report

## Status

The manuscript is submission-ready. Front matter, back matter, and a reproducible build pipeline now exist. One decision remains open for the author: the submission package itself (see **Open decisions**).

## Corrected word count

**80,847 words.** This supersedes every earlier figure in this repository.

`scripts/word_count.py` excluded all standalone italic lines as metadata. That rule was written to skip the `*POV:*` marker and old stub status lines, but it also silently dropped ten italicised in-world documents totalling 479 words: Sejanus's letter, Pontius's letter to Rome, his written orders at the standards retreat and Gerizim, Claudia's two tribunal messages, the closing tribunal summary, and Tamar's account letter from Caesarea.

Those are prose the reader reads. The counter now excludes only italic lines whose content begins with a metadata key (`POV`, `Status`, `Target`, `Word count`). `scripts/build_manuscript.py` independently counts the compiled output and agrees at 80,847, which gives the figure two sources.

The book remains inside the 80,000–85,000 target. For submission, round to 81,000.

## Copyedit pass

First line-level pass on this manuscript. Prior checks were structural, historical, or pattern-matched.

**Clean on inspection:** no doubled words, no double spaces, no trailing whitespace, no ellipses, no numerals in narration, no dialogue-attribution punctuation errors, consistent italic usage, every chapter carrying two or more scene sections.

**Corrected:**

| Issue | Detail |
|---|---|
| Eighteenth editorial artifact | `21-into-jerusalem.md` read "the chain later used in the Prologue." The consistency pass searched for `Chapter [0-9]+` and `next chapter` but not `Prologue`. Rewritten to "the chain by which a household message could reach the tribunal." |
| Character name collision | **Varro** named both a Germania centurion in Chapter 2 and Lucius Varro, the governor's legal scribe and a major Passion Week figure with sixty-one mentions. The centurion, a two-mention walk-on, is renamed **Priscus**. |
| Near-identical names | **Mattithiah** (Chapter 5, a gray-bearded priestly steward) and **Mattathias** (Chapters 18–26, a junior Temple scribe) are different characters two letters apart, both Temple intermediaries carrying messages to Claudia. Mattithiah, confined to one chapter, is renamed **Yoezer**. |
| Spelling variant | Two instances of **Judea** against twenty-eight of **Judaea**. Normalized to Judaea per `STYLE.md`. |

## Chapter length: resolved

Nine chapters finish below their `OUTLINE.md` projection, three materially (Chapter 10 by 340 words, Chapter 3 by 306, Chapter 11 by 289). Each was checked line by line against its outline row.

All three satisfy every required element. Chapter 3 delivers household footing, Roman-versus-local custom across the wage roll, the Sabbath rota and the kitchen, Tamar's revelation of both custom and mistrust, and the reversed punitive dismissal, across five sections. Chapter 10 delivers concealed soldiers, crowd panic, blocked access, immediately diverging accounts, aid moved, a witness protected, violence not stopped, and the cost made personal. Chapter 11 delivers the private casualty ledger and the one limited administrative concession.

The chapters are short because the prose is economical, not because a beat is missing. No words were added. `OUTLINE.md` now records that its per-chapter ranges were pre-draft projections superseded by delivered lengths.

## New assets

| Path | Purpose |
|---|---|
| `front-matter/00-title-page.md` | Standard manuscript title page |
| `front-matter/01-dramatis-personae.md` | Cast list by household and faction. Optional; some editors prefer none. |
| `back-matter/author-note.md` | Author's note, ~1,300 words |
| `scripts/build_manuscript.py` | Compiles submission deliverables |
| `build/the-wife-of-pontius-pilate.md` | Single-file Markdown |
| `build/the-wife-of-pontius-pilate.docx` | Standard manuscript format |

### On the author's note

Historical fiction working this close to a contested record needs one, and this book needs it more than most: the consistency pass removed twelve passages where the narrator stepped out of the story to discuss surviving sources and adopted traditions. That material was correct and belongs to the book. It simply belongs here rather than mid-scene.

The note states plainly what rests on Matthew 27:19 alone, that Claudia's name is later tradition, that Josephus and Philo are hostile witnesses, and that four load-bearing choices are disputed: the A.D. 33 crucifixion, the tribunal's location, the release custom, and the handwashing. It names the invented households and closes on the unknown later lives.

### On the build

`build_manuscript.py` never modifies `manuscript/`. It strips `*POV:*` markers, assembles front matter, thirty-one chapters, and the author's note, and renders in-chapter `## Section` headings as centered scene breaks, which is conventional for a submitted novel. Pass `--keep-section-titles` to preserve them as visible headings instead.

**This is an author decision.** The section titles are often good ("Clubs Beneath Cloaks", "What the Stones Kept") and some are working labels ("Three Reports", "Conditions"). Named subsections inside chapters are unusual in commercial fiction and can read as nonfiction structure. The default is scene breaks; one flag reverses it, and the source files retain every title either way.

## Verified at build

- 31 chapter headings, Prologue through Epilogue
- 180 scene breaks
- Title page carrying author, corrected word count, and title
- Author's note present
- Standard manuscript format: Times New Roman 12pt, double-spaced, one-inch margins, half-inch paragraph indent, no space between paragraphs, running header with surname, title, and automatic page number, each chapter opening on a new page
- Zero em dashes, zero editorial artifacts, zero "procurator"
- Both word counters independently agree

## Open decisions

1. **Submission route.** A query letter and synopsis (agent route) and cover copy with keyword metadata (self-publishing route) are different documents. Not written pending the author's direction.
2. **Section titles.** Default is scene breaks. Reversible with one flag.
3. **Dramatis personae.** Included as an asset; not every editor wants one in a submission.
4. **Contact details.** The title page carries a placeholder.

## Not done, and why

No line-by-line stylistic rewrite of the prose. The book has a deliberate and consistent voice, and the sentence-level texture is the author's. This pass corrected errors and inconsistencies; it did not impose taste.
