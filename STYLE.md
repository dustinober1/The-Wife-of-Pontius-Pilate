# Style Sheet

Conventions derived from the drafted prose (Prologue, Ch1, Ch2). These are descriptive of what the book already does — follow them so Ch3–29 read as the same book. Structural/file conventions live in CLAUDE.md; this file is about the prose itself.

## Narration

- **Close third, past tense.** One POV per chapter (assignments in OUTLINE.md). The narrator knows only what the POV character perceives or infers.
- **Direct interior thought** is set in italics, present tense, used sparingly — once or twice a chapter at most: *He thinks this is a simple hearing.* Everything else stays in narrated past.
- **Scene headings** (`##`) are short title-case noun phrases, evocative rather than literal ("The Knife-Edge Moment," "Lines on a Map"). Start from the Key Beats in OUTLINE.md where they fit.
- **Sensory grounding:** every scene opens with at least one concrete physical anchor (heat, smell, sound) before dialogue or politics. This is the book's most consistent habit — keep it.

## Diction and anachronism policy

- **No modern idiom, no modern abstractions** (no "seconds"/"minutes" as clock units, no "percent," no psychological jargon). Time runs on Roman hours ("before the ninth hour"), watches, feast days, and seasons. Natural idioms like "the moment the words sank in" are fine.
- **Familiar English units are allowed in narration** for readability — "forty yards," "three weeks" (both already on page). Don't switch to paces/stadia mid-book.
- **Metaphors stay inside the period and inside the POV character's world.** Claudia reasons in water, ink, thresholds, households; Pontius in roads, ledgers, engineering, drill. This differentiation is doing real work — protect it in the Pontius POV chapters.
- **Latin and Greek terms are set in roman type, not italics**, and used as ordinary nouns without glossing: palla, stola, tunic, domus, tablinum, peristyle, caligae, pilum, bema, Lithostrotos. Context carries the meaning; never stop to translate.
- Form of address: **"Domina"** from servants and inferiors; "Mistress" appears once in the Prologue from Marcus — prefer "Domina" going forward for consistency.

## Names

- **Pontius**, not "Pilate," in narration — both Claudia's chapters and his own. "Pontius Pilate" only at formal first mentions (as in Ch2); "the Prefect" / "the Governor" in official or crowd contexts.
- **Jesus is held at a distance**: "the Galilean," "the Galilean preacher," "the man from the dream," "Jesus of Nazareth" in formal register. He is seen through others and across space, never entered as a POV or given interiority. The offstage handling of John the Baptist (rumor, then news) is the model.
- **Sejanus, Tiberius, Caiaphas, Antipas, Herodias, Vitellius** by single name after introduction.

## Dialogue

- Standard American punctuation — commas and periods **inside** closing quotes. (The Prologue has four instances of `".` to normalize; fixed in the manuscript as of this sheet.)
- No dialect spellings, no Latin phrases dropped into speech for flavor. Register does the work: Pontius speaks in assertions and figures; Claudia in questions and images; servants briefly and concretely.
- Scripture is **paraphrased, never quoted**. The warning note deliberately paraphrases Matthew 27:19 ("Have nothing to do with that innocent man, for I have suffered much today because of a dream") — keep this approach for any Gospel-adjacent lines in Ch21–24. The faith arc must stay dual-readable (see CLAUDE.md); avoid liturgical vocabulary in Claudia's interiority.

## Punctuation and mechanics

- **No em dashes anywhere** (see CLAUDE.md, which supersedes this sheet's earlier "unspaced em dash" guidance from before the manuscript-wide no-em-dash pass). Rewrite with a period, comma, colon, or parenthetical instead. As of the em-dash sweep, zero em dashes remain anywhere in `manuscript/*.md` — keep it that way.
- Ellipses are also avoided throughout, by the same logic as em dashes (a trailing-off can be conveyed by ending the sentence and letting the next line's action carry the pause). Don't introduce one to indicate a character trailing off; use a full stop and a beat of action/description instead.
- **Quotes stay straight in the source** (`"` and `'`), which is standard for plain-text/Markdown editing and diffing. The docx export (`build.js` in the working scratchpad) converts them to typographic curly quotes (“ ” ‘ ’) at generation time — don't hand-convert the `.md` files themselves.
- Numbers spelled out in narration ("forty yards," "eleven years," "tens of thousands").
- Italics are reserved for interior thought only (see above) — not for emphasis, not for foreign terms.

## Recurring-thread discipline

The five threads (water/reflection, ink-stained hands, the map, Marcus's reactions, the dream) are catalogued in CLAUDE.md and OUTLINE.md. Style rule: **each appearance must be doing scene work, not signaling**. The fountain in Ch1 works because Claudia is actually looking at it while deciding something. If a thread appearance could be cut without the scene losing anything, cut it — an unused appearance cheapens the payoff. One touch per thread per chapter is the ceiling, and most chapters should touch none.
