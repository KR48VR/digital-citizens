# Casebook page template

The source of the private "Digital Citizens Casebook" page: how the study was done, the QA log, King and AI
(how King and Claude worked together), and the playbook package.

| File | What it holds |
|---|---|
| `template.html` | The page, with `{{PLACEHOLDERS}}` for tables, counts and examples. |
| `facts.json` | Each side's part in every task, the chosen examples of each kind of interaction, and the counts. |
| `build_casebook.py` | Fills the template from `facts.json`, `../../records/interactions.json` and `../../records/qa_log.json`; writes `casebook.html`. |
| `build_package.py` | Renders the playbook, glossary, checklist, notes and skills as pages in `package/` (needs the `markdown` package). |

## Rebuilding

1. Add new interactions to `records/interactions.json` (see `records/annotate_interactions.py` for the
   three kinds: tool, teammate, independent) and new findings to `records/qa_log.json`.
2. Update the counts and task parts in `facts.json`.
3. Run `python build_casebook.py` and `python build_package.py`.
4. Check at 375 px and 1,100 px, light and dark, with `../../qa_checklist.md`.
5. Publish `casebook.html` with the Artifact tool to the existing casebook link, passing the `package/`
   pages as `files` so the package links keep working.
