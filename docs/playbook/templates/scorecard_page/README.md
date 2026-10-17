# Scorecard page template

The source of the "How to use AI for digital citizens" page, split so it can be edited and rebuilt.

| File | What it holds |
|---|---|
| `body.html` | The page content. `{{CHART}}` marks where the bar chart goes. |
| `style.css` | Layout and type styles. |
| `tokens.css` | Colour tokens for light and dark mode (text contrast checked at 4.5:1 or better). |
| `build_page.py` | Draws the chart from its data, puts the parts together and writes the page. |

## Rebuilding

1. Edit `body.html` for the words and `rows = [...]` in `build_page.py` for the chart
   (country, group, chatbot kind % less error, record citizens % less error; 0 or below reads "more error").
   Take the percentages from unrounded results (`scripts/standout_split.py` prints them).
2. Run `python build_page.py out.html` (default output: `scorecard.html` next to the script).
3. Check the page at 375 px and 1,100 px wide, in light and dark, with `docs/playbook/qa_checklist.md`.
4. Publish with the Artifact tool. To keep the same link, publish to the existing page's URL.

Design rules kept by this template: one reading column; agreed terms only; definitions before use; every
number followed by its meaning; chatbot kind in orange, record citizens in green; text contrast at least
4.5:1; headings in order; captions on every table; the chart labelled directly; tables fit a phone screen.
