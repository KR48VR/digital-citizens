# QA checklist for a reader-facing page

## Accuracy
- [ ] Every number traces to a file in docs/results or a computation you can rerun; note the source.
- [ ] Rounding is consistent ("about 3 points off" covers 2.7 to 2.9).
- [ ] "As accurate as" claims say "about" unless the numbers are equal.
- [ ] Named example groups are checked in the data (which group stands out most often).
- [ ] Survey dates and fieldwork windows are stated where timing matters.
- [ ] No claim of an untested capability.
- [ ] The same number is the same everywhere on the page.

## Language
- [ ] Every term is defined before first use, with the one example person where possible.
- [ ] Only glossary terms; none of the "do not use" list.
- [ ] Each number is followed by what it means for the reader (the so-what).
- [ ] No sentence left "hanging": every note sits next to the thing it explains.

## Accessibility
- [ ] Text contrast at least 4.5:1 in light and dark (labels and table headers included).
- [ ] Headings go in order (h1, h2, h3) without skipping.
- [ ] Tables have captions; charts have an aria-label with every value and a table view.
- [ ] Chart series are told apart by more than colour (direct labels).
- [ ] Keyboard focus is visible; motion respects reduced-motion.
- [ ] No sideways scrolling at 375 px; text in charts readable on a phone.

## Aesthetics
- [ ] One accent per job (chatbot orange, record citizens green) used the same way throughout.
- [ ] Repeated elements share spacing and alignment; no orphaned headings.
- [ ] Dark mode checked, not just light.
