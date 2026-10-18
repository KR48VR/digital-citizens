"""Render the repo's playbook files as standalone pages for the casebook's package section."""
import html
import re
import sys
from pathlib import Path

import markdown

REPO = Path(__file__).resolve().parents[4]  # the repository root (casebook_page, templates, playbook, docs, root)
OUT = Path(__file__).resolve().parent / "package"  # published next to the casebook as package/*.html
BACK = sys.argv[1] if len(sys.argv) > 1 else "../"
FILES = [  # (published name, repo path, title)
    ("playbook.html", "docs/playbook/playbook.md", "Playbook"),
    ("glossary.html", "docs/playbook/glossary.md", "Agreed language"),
    ("qa_checklist.html", "docs/playbook/qa_checklist.md", "QA checklist"),
    ("working_with_king.html", "docs/playbook/working_with_king.md", "Working with King"),
    ("skill_digital_citizens_study.html", ".claude/skills/digital-citizens-study/SKILL.md", "Skill: digital-citizens study"),
    ("skill_c_suite_explainer.html", ".claude/skills/c-suite-explainer/SKILL.md", "Skill: C-suite explainer"),
    ("scorecard_template.html", "docs/playbook/templates/scorecard_page/README.md", "Scorecard page template"),
    ("index_readme.html", "docs/playbook/README.md", "Package index"),
]

CSS = """
:root { --bg: #f8f7f4; --surface: #fdfdfc; --ink: #0b0b0b; --ink-2: #3d3c39; --muted: #6b6a65; --grid: #e4e3dd; --accent: #1f5fae; color-scheme: light; }
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) { --bg: #121211; --surface: #1a1a19; --ink: #f0efec; --ink-2: #c3c2b7; --muted: #9a9890; --grid: #2c2c2a; --accent: #5aa0ee; color-scheme: dark; } }
:root[data-theme="dark"] { --bg: #121211; --surface: #1a1a19; --ink: #f0efec; --ink-2: #c3c2b7; --muted: #9a9890; --grid: #2c2c2a; --accent: #5aa0ee; color-scheme: dark; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink-2); font: 16px/1.6 "IBM Plex Sans", system-ui, sans-serif; }
main { max-width: 760px; margin: 0 auto; padding: 32px 16px 64px; }
h1, h2, h3 { color: var(--ink); font-family: "Source Serif 4", Georgia, serif; font-weight: 600; line-height: 1.25; }
h1 { font-size: 32px; margin: 8px 0 16px; } h2 { font-size: 22px; margin-top: 32px; } h3 { font-size: 18px; }
a { color: var(--accent); }
.back { font-size: 14px; }
.src { font-size: 13px; color: var(--muted); }
code { font: 14px ui-monospace, Menlo, monospace; background: var(--surface); border: 1px solid var(--grid); border-radius: 4px; padding: 1px 4px; overflow-wrap: anywhere; }
pre { background: var(--surface); border: 1px solid var(--grid); border-radius: 6px; padding: 12px; overflow-x: auto; }
pre code { border: 0; padding: 0; }
.tw { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { text-align: left; vertical-align: top; padding: 8px 8px; border-bottom: 1px solid var(--grid); }
th { color: var(--muted); font-size: 12px; text-transform: uppercase; letter-spacing: 0.04em; }
td:first-child { color: var(--ink); }
.meta { background: var(--surface); border: 1px solid var(--grid); border-radius: 6px; padding: 12px 14px; font-size: 14px; }
li { margin: 4px 0; }
"""


def render(name: str, src: str, title: str) -> None:
    text = (REPO / src).read_text()
    meta = ""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if m:  # skill front matter: show it as a small header block
        fields = dict(line.split(": ", 1) for line in m.group(1).splitlines() if ": " in line)
        meta = ('<div class="meta"><strong>When Claude Code uses this skill</strong><br>'
                f'{html.escape(fields.get("description", ""))}</div>')
        text = text[m.end():]
    body = markdown.markdown(text, extensions=["tables", "fenced_code", "sane_lists"])
    body = body.replace("<table>", '<div class="tw"><table>').replace("</table>", "</table></div>")
    page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,600&family=IBM+Plex+Sans:wght@400;600&display=swap">
<style>{CSS}</style>
</head>
<body>
<main>
<a class="back" href="{html.escape(BACK)}" onclick="if (history.length > 1) {{ history.back(); return false; }}">&larr; Back to the Digital Citizens Casebook</a>
<p class="src">From the repository: <code>{html.escape(src)}</code></p>
{meta}
{body}
</main>
</body>
</html>
"""
    (OUT / name).write_text(page)


OUT.mkdir(exist_ok=True)
for f in FILES:
    render(*f)
(OUT / "interactions.json").write_text((REPO / "docs/playbook/records/interactions.json").read_text())
print("package written:", ", ".join(f[0] for f in FILES), "+ interactions.json")
