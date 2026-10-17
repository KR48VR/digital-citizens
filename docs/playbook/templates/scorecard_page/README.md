# Scorecard page template

The source of the "How to use AI for digital citizens" page, split so it can be edited and rebuilt.

| File | What it holds |
|---|---|
| `body.html` | The page content. `{{CHART}}` marks where the bar chart goes. |
| `style.css` | Styles. Colours come from the theme tokens at the top of the built page. |
| `build_page.py` | Draws the chart from its data, adds the tokens and writes the page. |

## Rebuilding

The build script reads the colour tokens from an existing built page and writes to a fixed path. To reuse it:

1. Copy these three files to a working folder.
2. Edit the paths at the top of `build_page.py` (`F` = output page, and the folder holding `body.html` and `style.css`).
3. Change the chart rows in `build_page.py` (`rows = [...]`: country, group, chatbot %, record citizens %).
4. Run `python build_page.py`, then check the page at 375 px and 1,100 px, in light and dark, with
   `docs/playbook/qa_checklist.md`.
5. Publish with the Artifact tool to the same link to keep the address.

Design rules kept by this template: one reading column; agreed terms only; definitions before use; every
number followed by its meaning; chatbot kind in orange, record citizens in green; text contrast at least
4.5:1; headings in order; captions on every table; the chart labelled directly.
