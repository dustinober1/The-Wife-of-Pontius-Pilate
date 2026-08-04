# Cover Design Brief

No cover art exists yet; this is nothing but words. Hand this to a
freelance designer (Reedsy, 99designs, a direct commission) or use it
yourself in a DIY cover tool (Canva, BookBrush, KDP's own cover creator).
Once you have final art, `scripts/build_epub.py --cover path/to/cover.jpg`
embeds it in the ebook; the print wraparound cover (front, spine, back)
is a separate file KDP generates a template for once trim size and final
page count are locked (see `retail/kdp-metadata.md`).

## The one-sentence brief

A Roman woman's face turned away from the viewer, or not shown at all;
water, ink, or a map standing in for her the way the novel itself does.

## Comparable covers, for visual reference

- *Wolf Hall* (Hilary Mantel), UK Fourth Estate edition: a single
  Holbein-derived portrait detail, restrained typography, muted palette.
  Look at how little the cover tells you and how much weight the
  typography carries instead.
- *Imperium* / *Pompeii* (Robert Harris): classical architecture or
  statuary rendered in a single dominant color, bold serif title, author
  name equally prominent (Harris is the sell).
- *The Testament of Mary* (Colm Tóibín): a plain, almost devotional
  simplicity. No crowd scenes, no battle imagery. One figure or one
  object.

Avoid: a bearded man on a cross rendered literally (this book is
deliberately not about him, and readers picking it up for Claudia's story
will be misled by devotional cover art); a generic toga-and-sandals stock
photo (signals cheap ancient-world pulp, not literary historical
fiction); anything busy with multiple figures fighting for the eye in a
thumbnail-sized Amazon listing.

## Imagery drawn from the book itself

The novel has a small set of recurring images that do real work in the
text (`CLAUDE.md` calls them out explicitly: water and reflection,
ink-stained hands, a map, and the recurring dream). Any of these is a
more honest cover concept than generic Roman imagery:

- **Water.** Appears at the opening (Claudia waking from the dream),
  runs through Pontius's handwashing at the very end, and recurs as a
  basin, a fountain, the sea crossing. A single basin of dark water with
  a hand's reflection, or just water catching light against black, would
  visually rhyme with the book's actual close.
- **Ink-stained hands.** Claudia's guardian's lesson to her as a child;
  her own hand throughout the book, always writing, comparing, marking
  records. A hand, ink on the fingers, over parchment or a wax tablet, is
  specific to this character rather than to "ancient Rome" generally.
- **A map.** Used repeatedly for the province, the roads, the political
  geography Pontius trusts and Claudia complicates. A partial map of
  Judaea under a hand or a lamp, roads picked out in a single accent
  color, reads as political thriller rather than costume drama.
- **The judgment seat (bema).** An empty raised platform, stone steps,
  seen from behind or from a high angle (Claudia's terrace vantage,
  which is how the reader first sees the tribunal in the Prologue) rather
  than a crowd shot. Empty of figures, it is ominous without being
  literal.
- **A robed woman seen from behind or at a distance**, on a terrace or
  balcony looking down, small against Roman architecture. This visually
  states "she watches, she does not command" in one image, which is the
  entire premise of the book.

## Typography direction

- Title face: a classical, slightly condensed serif (something in the
  Trajan / Optima / Bembo family communicates "Rome" without resorting to
  a costume-drama script face). Avoid anything that reads as biblical
  epic movie poster (heavy gold, ornate flourish) unless you are
  deliberately positioning toward the Christian/biblical fiction shelf
  rather than literary historical fiction; the two audiences read very
  different type treatments as "for me."
- Author name: comparable size to the title or only modestly smaller.
  This is a debut, so the title is the sell, but don't bury the name.
- Subtitle "a novel" in a small italic, if used at all, sits under the
  title, matching the interior title page.

## Palette

Options in order of how well they match the book's own imagery:

1. **Deep water blue-black with one warm accent** (lamp-oil gold, or the
   dull red of a broken wax seal) for a single focal object or line of
   text. Matches the water/ink motif and reads as serious literary
   fiction on a shelf, not devotional.
2. **Stone and sand neutrals** (limestone, terracotta, faded ochre) with
   dark ink-black type, evoking Caesarea and Jerusalem architecture
   without costume cliché.
3. Avoid: purple-and-gold (reads as generic "biblical epic"), pure white
   backgrounds with a single small icon (reads as cozy/inspirational,
   wrong tone for a political thriller).

## Back cover / spine

- Back cover copy: use the book description in `retail/kdp-metadata.md`
  verbatim or lightly trimmed to fit the template your printer or
  designer supplies.
- Spine: title, author name, and (if you have one) a publisher/imprint
  mark. Spine width depends on final page count; do not lock it until
  `scripts/build_print_interior.py` reports a final page count against
  the front and back matter you actually intend to ship (dedication,
  acknowledgments, and about-the-author are still placeholders as of
  this writing, and filling them in will shift the count slightly).
- Consider a short pull quote or the epigraph line
  ("*Have nothing to do with that innocent man...*") set small on the
  back cover above the description; it is public domain (KJV) and gives
  a browsing reader the book's central image before they read a word of
  copy.
