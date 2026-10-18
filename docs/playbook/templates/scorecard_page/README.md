# Scorecard page template

The source of the "How to use AI for digital citizens" page, split so it can be edited and rebuilt.

| File | What it holds |
|---|---|
| `body.html` | The page content. `{{CHART}}` marks where the bar chart goes. |
| `style.css` | Layout and type styles. |
| `tokens.css` | Colour tokens for light and dark mode (text contrast checked at 4.5:1 or better). |
| `build_page.py` | Draws the chart from its data, puts the parts together and writes the page. |

## Rebuilding

1. Run `scripts/one_method_experiment.py singapore 10` and `... us 10` to produce the results the page reads.
   Edit `body.html` for the words. Numbers go in as `{{PLACEHOLDERS}}`, filled by `build_page.py` from the
   results; the chart and tables are drawn from the same files. Wording such as "about a sixth" is checked
   in `CHECK` and printed when you build.
2. Run `python build_page.py out.html` (default output: `scorecard.html` next to the script).
3. Check the page at 375 px and 1,100 px wide, in light and dark, with `docs/playbook/qa_checklist.md`.
4. Publish with the Artifact tool. To keep the same link, publish to the existing page's URL.

Design rules kept by this template: one reading column; five numbered sections on colour bands, matched in the
contents bar; agreed terms only; each term explained where first met; every number followed by its meaning and
linked to its evidence; survey alone in grey, chatbot kind in orange, record citizens in green; text contrast at least
4.5:1; headings in order; captions on every table; the chart labelled directly; tables fit a phone screen; every number from one test.
