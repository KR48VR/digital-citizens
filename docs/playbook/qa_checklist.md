# QA checklist for a reader-facing page

## Accuracy
- [ ] Every number traces to a file in docs/results or a computation you can rerun; note the source.
- [ ] Rounding is consistent ("about 3 points off" covers 2.7 to 2.9).
- [ ] "As accurate as" claims say "about" unless the numbers are equal.
- [ ] Named example groups are checked in the data (which group stands out most often).
- [ ] Survey dates and fieldwork windows are stated where timing matters.
- [ ] No claim of an untested capability.
- [ ] The same number is the same everywhere on the page.
- [ ] Percentages and differences are computed from unrounded values, and each figure is rounded once.
- [ ] Every label matches what was computed (a "standout groups" row really is the standout groups).
- [ ] Every headline number comes from one setup (same draws, same questions, same comparison). If two
      sections need different setups, say so on the page and keep the second to the analysts' section.
- [ ] Each result is credited to the method that produced it (record citizens alone, or pooled with the chatbot).
- [ ] Every example uses a question that is actually in the data.
- [ ] Nothing is generalised from a handful of cases; small counts are stated or the claim is dropped.
- [ ] Causes are framed as "the likely reason" unless they were tested.
- [ ] Simpler alternatives that did about as well are mentioned, not hidden.
- [ ] An independent helper agent recomputes every number from the raw results before sharing.

## Language
- [ ] Every term is defined before first use, with the one example person where possible.
- [ ] Only glossary terms; none of the "do not use" list.
- [ ] Each number is followed by what it means for the reader (the so-what).
- [ ] No sentence left "hanging": every note sits next to the thing it explains.
- [ ] Cold read: a helper agent playing an executive with no stats background reads the page with folds
      closed, answers what the finding is, what to do with a 300-person budget and what to watch out for,
      and lists every phrase it had to reread. Fix those, then repeat until it can act on one read.
- [ ] No two statements on the page seem to contradict each other (for example "reuse" versus "don't borrow").
- [ ] The main path stays short: detail that only some readers need sits in a folded section, not in the flow.

## Accessibility
- [ ] Text contrast at least 4.5:1 in light and dark (labels and table headers included).
- [ ] Headings go in order (h1, h2, h3) without skipping.
- [ ] Tables have captions; charts have an aria-label with every value and a table view.
- [ ] Chart series are told apart by more than colour (direct labels).
- [ ] Keyboard focus is visible; motion respects reduced-motion.
- [ ] No sideways scrolling at 375 px; text in charts readable on a phone; every table column visible
      without scrolling inside the table.

## Aesthetics
- [ ] One accent per job (chatbot orange, record citizens green) used the same way throughout.
- [ ] Repeated elements share spacing and alignment; no orphaned headings.
- [ ] Dark mode checked, not just light.

## Log
- [ ] Every finding goes into the QA log with when, area, finding, fix and status.
