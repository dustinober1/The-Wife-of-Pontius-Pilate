# CLAUDE.md

## Repository authority

This repository is the sole manuscript and editorial source of truth for *The Wife of Pontius Pilate*. `OUTLINE.md` governs structure, `CHARACTERS.md` governs character continuity, `TIMELINE.md` governs chronology, `STYLE.md` governs prose, and `editorial/historical-uncertainty-register.md` governs the status of historical claims.

## Current manuscript state

- Drafted prose: Prologue and Chapters 1–26.
- Undrafted outline stubs: Chapters 27–29 and the Epilogue (`30`).
- Current drafted baseline: **69,368 prose words**, counted with `python3 scripts/word_count.py` during Batch 8 verification.
- Finished target: approximately **80,000–85,000 words**, never below 65,000.

Do not replace a stub with prose unless the task explicitly authorizes that chapter. Do not create duplicate chapter files.

## Governing dramatic premise

A politically intelligent Roman woman gradually realizes that the systems of power surrounding her husband are converging on the execution of an innocent man, and every attempt she makes to restrain those systems risks her marriage, her security, and her husband’s standing with Rome.

The catastrophe arises from interacting institutions and rational self-interest, not a single hidden conspiracy: Roman vulnerability, Pontius’s fear of complaint, Temple authority, Herodian rivalry, jurisdictional ambiguity, incomplete intelligence, Passover crowd pressure, personal leverage, and institutional self-protection.

## POV and chapter authority

Close third person, past tense, one POV per chapter. Claudia is the default. Pontius POV is limited to Chapters 4, 6, 9, 15, 16, 19, 25, and 28 unless the outline is formally revised first. Jesus and John the Baptist never receive POV.

## Claudia’s operational spine

Claudia develops from observer to limited political actor through historically plausible household access. Her practice includes comparing rumor with dispatches, reading omissions, examining accounts, cultivating servants and wives as partial sources, using Marcus as an administrative messenger, using Tamar for lived local perception, directing limited relief funds, deciding what to tell or conceal from Pontius, and accepting marital risk. She is not a magistrate, spy chief, universal confidante, or infallible analyst. She must make mistakes and must alter some outcomes before Passion Week without controlling major history.

## Pontius’s tragic spine

His creed is “an even hand and an unbending spine.” Standards teach him that identity can outrank survival; retreat becomes humiliation; the aqueduct becomes a technical solution; the riot teaches procedural rationalization; Sejanus rewards it; John’s death models fear renamed necessity; Sejanus’s fall removes protection; Caiaphas gains leverage; Pontius governs to prevent complaints; Passover creates simultaneous risks; the tribunal turns every option dangerous; he chooses institutional survival through moral evasion; Gerizim completes the corruption of his original theory.

## Information channels

- **Marcus:** enslaved Greek household secretary/steward, literate administrative observer, recorder, scheduler, messenger, and document handler. His access is real and dangerous but limited to household and prefectural movement.
- **Tamar:** free local household worker, moral and cultural interlocutor, and source for ordinary provincial perception. Her knowledge is local, partial, relational, and sometimes wrong. She is not a covert operative or exposition device.

## Historical restraint

Use `editorial/historical-uncertainty-register.md`. Disputed matters must be labeled in planning rather than presented as settled fact. Pontius’s historical title is **prefect**. Claudia’s name, Sejanus’s personal role in the appointment, John’s death date, exact tribunal geography, release custom, and Pontius’s later fate require explicit qualification.

## Recurring threads

Water/reflection, ink-stained hands, the map, Marcus’s reactions, and the dream must perform scene work rather than announce themes. The dream progresses from ambiguous disturbance to sharper recurrence to Passion Week nightmare; it never functions as proof.

## Prose constraints

- No em dashes in new or revised prose. Use periods, commas, colons, or parentheses.
- Avoid negative parallelism such as “not X, but Y.”
- Avoid rule-of-three inflation, explanatory symbolism, vague attribution, modern abstractions, and narration that summarizes a scene’s meaning.
- Sensory detail must support pressure, choice, or orientation rather than substitute for escalation.
- Scripture is paraphrased rather than quoted at length.

## Word count

Run:

```bash
python scripts/word_count.py
python scripts/word_count.py --json
```

The utility excludes outline-only stubs, Markdown headings, blockquoted stub metadata, and standalone italic metadata.

## Revision workflow

Revise in manuscript order unless `editorial/revision-execution-sequence.md` authorizes a dependency-driven exception. Before revising any drafted chapter, follow its lock in `editorial/chapters-00-17-revision-mission-locks.md`. Before drafting Chapter 18, follow `editorial/chapter-18-mission-lock.md`.
