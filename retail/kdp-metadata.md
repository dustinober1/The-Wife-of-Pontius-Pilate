# KDP Publishing Metadata

Everything on this page needs a final human pass before upload; treat it as a
strong first draft, not copy to paste blind. Amazon renames category paths
and adjusts keyword rules periodically, so verify current wording in the
KDP dashboard at the time you publish.

## Book description (back-cover / product page copy)

This is the sales copy for the Amazon product page and, if you want, the
physical back cover. It is deliberately different from the synopsis in
`submission/synopsis.md`, which spoils the ending for query purposes; this
does not.

> Rome sends men to govern its provinces. It sends their wives along as an
> afterthought, expected to smooth dinners and keep silent about everything
> else.
>
> Claudia was raised from childhood to find the truth beneath a convenient
> lie. In Judaea she turns that gift into something no one gave her
> permission to have: a private channel into the councils, the Temple, and
> the household kitchens of a province her husband cannot fully see. For
> ten years it lets her save a few lives, protect a few servants, and
> correct a few lies before they harden into policy.
>
> Then a Galilean teacher is brought before her husband's tribunal on a
> morning during Passover, accused of a crime no witness can quite
> describe, and Claudia understands, faster than anyone else in the
> palace, exactly what is happening and why everything she has learned
> will not be enough to stop it.
>
> Built around the single line the historical record gives her, *Have
> nothing to do with that innocent man, for I have suffered much today
> because of a dream,* THE WIFE OF PONTIUS PILATE is a political thriller
> that needs no conspiracy, only people behaving reasonably, and a woman
> who can see the machine clearly enough to know she cannot climb inside
> it in time.

(196 words. KDP's description field supports basic HTML; wrap paragraphs
in `<p>` tags and italics in `<i>` tags when you paste it into the
dashboard, since Markdown is not rendered there.)

## Categories

KDP asks for up to three BISAC-style categories on the paperback listing
and up to two Amazon browse categories on the Kindle listing (interfaces
differ and change). Reasonable choices for this book, to verify against
the live dropdown at upload:

- Fiction > Historical > Ancient
- Fiction > Religious > Christian > Historical
- Fiction > Political

If those specific paths are not offered verbatim, the closest available
equivalents are what matters, not an exact string match. Historical
Fiction and Religious/Christian Fiction are almost certainly available;
Political Fiction is the one most likely to have moved or merged since
this was written.

## Keywords (seven, up to 50 characters each)

A draft starting point. Amazon's own search-suggest ("pontius pilate
novel...", "biblical historical fiction...") is a better source of truth
than any fixed list, since reader search phrasing shifts. Check it before
you finalize these.

1. biblical historical fiction novel
2. ancient rome political thriller
3. pontius pilate wife claudia
4. roman judea passion week novel
5. crucifixion story retold
6. jesus trial roman empire fiction
7. historical fiction strong woman

## Content notes

Adult readership. Contains depicted violence (a crowd suppression, a
riot, a scourging, a crucifixion), themes of slavery and its moral cost,
and a treatment of the Passion narrative that takes no position on the
resurrection's historicity while depicting characters who do. No explicit
sexual content. Worth a line in your own author's note to booksellers or
in review-copy outreach, since the subject matter draws both religious
and purely-historical-fiction readers and each audience benefits from
knowing what tone to expect.

## Trim, page count, and pricing

Print interior default: 5.5in x 8.5in, currently 383 pages with the front
and back matter placeholders (dedication, acknowledgments, about-the-author)
still unfilled. Page count will shift once those are written, and again if
you change trim size, font size, or margins; rerun
`scripts/build_print_interior.py` and check the reported count before
finalizing a cover spine width.

KDP calculates paperback royalty from list price minus printing cost, and
printing cost is driven by page count, trim, and ink (black and white
here). At roughly this length and trim, expect KDP's own price
calculator (visible during upload) to show a printing cost in the
neighborhood of a few dollars; comparable historical fiction paperbacks
of similar length commonly list between $14.99 and $17.99. Ebook pricing
for a debut in this category commonly runs $3.99 to $6.99 to stay inside
KDP's 70% royalty band (which requires pricing between $2.99 and $9.99
and some additional territory conditions). None of this is prescriptive;
it is orientation for where comparable books sit, and the final call is
yours.

## ISBN

KDP will assign a free ISBN to both the ebook and the paperback if you
publish exclusively through KDP and are comfortable with Amazon listed as
the ISBN's publisher of record ("Independently Published"). If you want
to distribute the paperback beyond Amazon (Ingram, other retailers) or
want your own name or imprint as publisher of record, buy your own ISBN
before upload, one for the paperback and a separate one if you also want
one for the ebook (ebooks distributed only through KDP do not strictly
need one). In the US this is Bowker (myidentifiers.com); other countries
have their own national ISBN agency. Once you have one, update
`front-matter/01-copyright-page.md` and rerun the builds.

## Series and edition

Standalone novel, no series. "First edition" is already set on the
copyright page; update it if you issue a revised edition later.
