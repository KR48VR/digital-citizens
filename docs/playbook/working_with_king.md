# How King and Claude work together

Distilled from the October 2026 digital-citizens session (about 130 messages from King over about a day).
Full record with every interaction: the Digital Citizens Casebook (private; access on request), "King and AI" section.

## What King wants from a page
- Plain, simple language for a C-suite reader. No jargon; if a term is needed, define it first.
- The same agreed terms throughout (see glossary.md). Changing a term confuses readers.
- One idea at a time, in an order where nothing is used before it is explained.
- Numbers with their meaning: what the number is, what it means, and so what.
- One running example (the 62-year-old woman) instead of many new ones.
- Claims backed by evidence, with the source named when asked.

## How King works
- Reviews the live page independently and sends screenshots with highlighted text.
- Asks short probing questions ("isn't 2.6 to 2.4 pretty good?", "is this backed up?", "was that during covid?").
  Treat each as a prompt to check the data, not to defend the wording.
- Often drafts wording and asks "should we say...". Keep King's intent, tighten grammar, explain any change.
- Says "discuss with me" when a decision is wanted before editing: give a view and options, then wait.
- Near the end, collects final comments and asks for one integrated pass ("stop patching"): make no edits
  between comments; then change the whole page at once and list every change with its new wording.
- Asks "why don't you say X?" when a workaround is more confusing than the plain term ("median" instead
  of "typical group"). Use the standard word, explained in one line.
- Chooses design options on practical grounds ("a team can say look at the green band"): show side-by-side
  mock-ups in light and dark mode, give a recommendation, and go with King's choice.

## What worked
- Admitting and correcting errors quickly, in the open (small-survey scoring, the untested chatbot claim,
  the over-60 example).
- Running a new test when King asked "why didn't we test X?" rather than explaining the gap away.
- Turning King's ideas into experiments (survey library, local data with Bayesian weighting, published findings).
- Recapping each change with the exact new wording.
- An independent audit by a helper agent that recomputed every number from the raw results. It caught a
  mislabelled "standout groups" row that changed what the page says about the chatbot in Singapore.
  Next time, run it before the page first goes to King, not only at the end.
- Keeping one method throughout. King spotted that the page mixed setups (a blend of both kinds of AI for
  the headline, a different comparison for the chatbot section). Rebuilding on one test changed one claim
  (standout groups) and confirmed the rest. Decide the single test before writing the page.
- One integrated pass against six agreed principles, followed by a short list of changes, after many small
  patches had moved problems around.
- A build check behind every new claim, so wording edits could not drift from the data.

## What to avoid
- Jargon in replies, not just on the page ("spread", "headline number", "exchange rate", "signal").
- Leaving notes or footnotes floating away from what they explain.
- Introducing a second concept in a sentence meant to explain the first.
- Overclaiming ("as accurately as" when it is "about as accurately as").
- Patching one comment at a time: moving "how to read the numbers" ahead of the two cases broke the flow
  from the summary.
- Showing the method's inner workings on the main path (fitted weights, worked sums): they do not help a
  first-time reader.
- A scenario example placed before the decision logic: readers could not tell when it applied.
