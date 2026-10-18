# Digital citizens package

Everything needed to run a digital-citizens study again, for a new country, city or question, or to pick
this one up later.

## The two pages

| Page | What it is | Who can open it |
|---|---|---|
| [How to use AI for digital citizens](https://claude.ai/artifact/1EfjB41MM2Nn69EwY5Ht45) | The scorecard for a C-suite reader: the short answer, the two kinds of AI, a decision tree, how we know, limits | Private; King shares it from the page's Share menu |
| [Digital Citizens Casebook](https://claude.ai/artifact/Pqi6H7QszpxTH9KjXi5Lz2) | How we did this, the QA log, King and AI (how King and Claude worked together), and this package | Private; access on request |

## Files

| File | What it is for |
|---|---|
| [playbook.md](playbook.md) | The method in eight steps, with code pointers and lessons learned |
| [glossary.md](glossary.md) | The agreed reader-facing terms, how to define them, and words to avoid |
| [qa_checklist.md](qa_checklist.md) | Accuracy, flow, language, accessibility and aesthetics checks before sharing |
| [working_with_king.md](working_with_king.md) | What King wants from a page, how King works, what worked |
| [templates/scorecard_page/](templates/scorecard_page/) | The scorecard page's source and build script |
| [templates/casebook_page/](templates/casebook_page/) | The casebook page's source and build scripts |
| [records/interactions.json](records/interactions.json) | Every interaction of the October 2026 session, with task and kind |
| [records/qa_log.json](records/qa_log.json) | Every QA finding on the scorecard, its fix and status |
| [../../.claude/skills/digital-citizens-study/SKILL.md](../../.claude/skills/digital-citizens-study/SKILL.md) | Skill: run or extend a study (loads automatically in Claude Code) |
| [../../.claude/skills/c-suite-explainer/SKILL.md](../../.claude/skills/c-suite-explainer/SKILL.md) | Skill: write for King and a C-suite reader (loads automatically) |

## Using it next time

1. Start a Claude Code session on this repository. The two skills load automatically.
2. Ask in plain words, for example "Run a digital-citizens study for Malaysia on this question" or
   "Add Taiwan and re-run the scorecard".
3. Claude follows the playbook, writes in the agreed language and runs the QA checklist before publishing.
4. To update either page, give Claude its link; Claude reads it first and keeps the same address.
