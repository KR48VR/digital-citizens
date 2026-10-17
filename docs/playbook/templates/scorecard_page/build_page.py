"""Build the scorecard page from body.html, style.css and tokens.css in this folder.

Usage: python build_page.py [output.html]   (default: scorecard.html next to this file)
Edit the chart data in `rows` below: (country, group, chatbot kind % less error, record citizens % less error).
A value of 0 or below draws a stub and reads "N% more error".
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "scorecard.html"
TITLE = "Digital Citizens Scorecard"

X0, PX = 0, 5.0  # 80% -> 400 user units; labels sit on their own line above each pair of bars
rows = [("United States", "most groups", 33, 42), ("United States", "standout groups", 68, 79),
        ("Singapore", "most groups", -4, 26), ("Singapore", "standout groups", 43, 40)]
def bar(x0, y, w, h, r, fill, tip):
    r = min(r, w / 2)
    d = f"M{x0} {y}H{x0+w-r:.1f}Q{x0+w:.1f} {y} {x0+w:.1f} {y+r}V{y+h-r}Q{x0+w:.1f} {y+h} {x0+w-r:.1f} {y+h}H{x0}Z"
    return f'<path class="bar" d="{d}" fill="{fill}" data-tip="{tip}" tabindex="0"/>'
svg = []
H, GAP, ROW = 16, 2, 74
for i, (c, g, cb, rc) in enumerate(rows):
    top = 4 + i * ROW
    svg.append(f'<text class="lbl" x="0" y="{top+18}"><tspan font-weight="600">{c}</tspan><tspan class="muted"> · {g}</tspan></text>')
    for j, (v, fill, who) in enumerate([(cb, "var(--s2)", "Chatbot kind"), (rc, "var(--s3)", "Record citizens")]):
        y = top + 26 + j * (H + GAP)
        if v <= 0:
            svg.append(f'<rect x="{X0}" y="{y}" width="2" height="{H}" fill="{fill}" data-tip="{c}, {g} · {who}: {abs(v)}% more error than No AI" tabindex="0"/>')
            svg.append(f'<text class="val" x="{X0+8}" y="{y+12.5}">{abs(v)}% more error</text>')
            continue
        w = v * PX
        svg.append(bar(X0, y, w, H, 4, fill, f"{c}, {g} · {who}: removes {v}% of the error"))
        svg.append(f'<text class="val" x="{X0+w+6:.1f}" y="{y+12.5}">{v}%</text>')
        if i == 0:
            svg.append(f'<text class="inbar" x="{X0+6}" y="{y+12.5}">{who}</text>')
grid = "".join(f'<line x1="{X0+p*PX:.0f}" y1="0" x2="{X0+p*PX:.0f}" y2="292"/>' for p in (20, 40, 60, 80))
ticks = "".join(f'<text x="{X0+p*PX:.0f}" y="308" text-anchor="{"start" if p == 0 else "middle"}">{p}%</text>' for p in (0, 20, 40, 60, 80))
def _pct(v):
    return f"{v}%" if v > 0 else f"{abs(v)}% more error"
aria = "Grouped bars: share of the error each kind of AI removes compared with No AI. " + " ".join(
    f"{c} {g}: chatbot {_pct(cb)}, record citizens {_pct(rc)}." for c, g, cb, rc in rows)
svg_body = "\n      ".join(svg)
chart = f'''<svg class="chart" viewBox="0 0 520 316" role="img" aria-label="{aria}">
      <g class="grid">{grid}</g>
      <g class="sub">{ticks}</g>
      {svg_body}
      <line class="axis" x1="{X0}" y1="0" x2="{X0}" y2="292"/>
    </svg>'''

tokens = (HERE / "tokens.css").read_text()
body = (HERE / "body.html").read_text()
css = (HERE / "style.css").read_text()
page = (f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">\n'
        '<style>\n  /* Layout: one reading column for a busy executive. Answer first, then the one idea that explains it, then the evidence, then rules and limits. Detail folded away. */\n'
        + tokens + css + "</style>\n" + body.replace("{{CHART}}", chart))
OUT.write_text(page)
print("written", OUT, len(page))
