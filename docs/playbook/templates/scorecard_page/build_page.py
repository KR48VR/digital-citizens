"""Build the scorecard page from body.html, style.css and tokens.css in this folder.

Usage: python build_page.py [output.html]   (default: scorecard.html next to this file)
The chart, the tables and every {{PLACEHOLDER}} number are read from the one-method results in
docs/results/stress_test/one_method_*.csv (run scripts/one_method_experiment.py first), so the page cannot
drift from the data. Statements in words ("about a sixth") are checked in CHECK and printed.
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "scorecard.html"
TITLE = "Digital Citizens Scorecard"

import csv
RES = HERE.parents[3] / "docs" / "results" / "stress_test"
SERIES = [("survey alone", "Survey alone", "var(--muted)"),
          ("+ chatbot kind", "+ chatbot kind", "var(--s2)"),
          ("+ record citizens", "+ record citizens", "var(--s3)")]
SIZES = (150, 300, 600)


def medians(tag):
    out = {}
    for r in csv.DictReader(open(RES / f"one_method_{tag}.csv")):
        out[(r["config"], int(r["n"]))] = float(r["median"])
    return out


def panel(country, data, ymax=6.0):
    W, PL, PR, PT, PB = 360, 30, 200, 14, 196
    xs = {n: PL + 18 + i * (PR - PL - 18) / 2 for i, n in enumerate(SIZES)}
    def y(v):
        return PB - v / ymax * (PB - PT)
    g = []
    for v in range(0, int(ymax) + 1, 2):
        g.append(f'<line class="grid" x1="{PL}" y1="{y(v):.1f}" x2="{PR}" y2="{y(v):.1f}"/>'
                 f'<text class="tick" x="{PL-6}" y="{y(v)+4:.1f}" text-anchor="end">{v}</text>')
    for n in SIZES:
        g.append(f'<text class="tick" x="{xs[n]:.1f}" y="{PB+18}" text-anchor="middle">{n}</text>')
    g.append(f'<text class="tick" x="{(PL+PR)/2:.1f}" y="{PB+34}" text-anchor="middle">people in the survey</text>')
    g.append(f'<line class="axis" x1="{PL}" y1="{PB}" x2="{PR}" y2="{PB}"/>')
    ends = []
    for key, label, colour in SERIES:
        pts = [(xs[n], y(data[(key, n)])) for n in SIZES]
        g.append(f'<polyline class="ln" points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" stroke="{colour}"/>')
        for n, (a, b) in zip(SIZES, pts):
            g.append(f'<circle class="pt" cx="{a:.1f}" cy="{b:.1f}" r="4.5" fill="{colour}" tabindex="0" '
                     f'data-tip="{country}, survey of {n} {label.replace("+ ", "+ ")}: {data[(key, n)]:.1f} points off"/>')
        ends.append([pts[-1][1], label, colour])
    ends.sort(key=lambda e: e[0])
    orig = [e[0] for e in ends]
    for i in range(1, len(ends)):  # nudge end labels apart, then centre the stack on the points
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + 15)
    shift = sum(orig) / len(orig) - sum(e[0] for e in ends) / len(ends)
    for (yy, label, colour), y0 in zip(ends, orig):
        yy = yy + shift
        g.append(f'<line class="key" x1="{PR+8}" y1="{y0:.1f}" x2="{PR+14}" y2="{yy:.1f}" stroke="{colour}"/>'
                 f'<line class="key" x1="{PR+14}" y1="{yy:.1f}" x2="{PR+24}" y2="{yy:.1f}" stroke="{colour}"/>'
                 f'<text class="end" x="{PR+28}" y="{yy+4:.1f}">{label}</text>')
    aria = f"{country}: points off for a typical group by survey size. " + " ".join(
        f"{label}: " + ", ".join(f"{data[(key, n)]:.1f} at {n}" for n in SIZES) + "." for key, label, _ in SERIES)
    return (f'<div class="panel"><p class="ptitle">{country}</p><svg class="lines" viewBox="0 0 {W} {PB+42}" role="img" aria-label="{aria}">'
            + "".join(g) + "</svg></div>")


SG, US = medians("singapore"), medians("us")
chart = '<div class="panels">' + panel("Singapore", SG) + panel("United States", US) + "</div>"


def f1(v):
    return f"{v:.1f}"


def pct(base, v):
    return round(100 * (base - v) / base)


def cut_txt(p):
    return f"{p}% less error" if p >= 0 else f"{-p}% more error"


import pandas as pd
CELLS = {t: pd.read_csv(RES / f"one_method_{t}_cells.csv") for t in ("singapore", "us")}
PER_CELL = {t: c.groupby(["config", "n", "question_id", "group"], as_index=False).agg(mae=("mae_pts", "mean"), ng=("n_group", "mean")) for t, c in CELLS.items()}


def group_val(tag, n, group, config):
    v = PER_CELL[tag]
    v = v[(v.n == n) & (v.group == group) & (v.config == config)]
    return v.mae.median(), v.ng.mean()


small_rows, SMALL = [], {}
for g, label, key in [("ethnic=Chinese", "Chinese Singaporeans", "CHI"), ("ethnic=Malay", "Malay Singaporeans", "MAL"), ("ethnic=Indian", "Indian Singaporeans", "IND")]:
    a_, ng = group_val("singapore", 150, g, "survey alone")
    r_, _ = group_val("singapore", 150, g, "+ record citizens")
    SMALL[key] = (f1(a_), f1(r_), round(ng))
    small_rows.append(f'<tr><td>{label}</td><td class="num">about {round(ng)}</td><td class="num"><b>{f1(a_)}</b></td><td class="num"><b>{f1(r_)}</b></td></tr>')
TABLE_SMALL = ('<div class="wrap">\n    <table class="pts">\n      <caption>Points off for each group, from a 150-person survey in Singapore</caption>\n'
               '      <thead><tr><th>Group</th><th class="num">People in the survey</th><th class="num">Survey alone</th><th class="num">With record citizens</th></tr></thead>\n      <tbody>\n        '
               + "\n        ".join(small_rows) + "\n      </tbody>\n    </table>\n    </div>")

kind_rows = []
for name, D in [("Singapore", SG), ("United States", US)]:
    for n in SIZES:
        base = D[("survey alone", n)]
        cells_ = [f'<td class="num"><b>{f1(base)}</b><span class="cut">starting point</span></td>']
        for key in ("+ chatbot kind", "+ record citizens"):
            cells_.append(f'<td class="num"><b>{f1(D[(key, n)])}</b><span class="cut">{cut_txt(pct(base, D[(key, n)]))}</span></td>')
        kind_rows.append(f'<tr><td>{name}<span class="cut">survey of {n}</span></td>' + "".join(cells_) + "</tr>")
TABLE_KINDS = ('<div class="wrap">\n    <table class="pts">\n      <caption>Points off for a typical group, and how much less error than the survey alone</caption>\n'
               '      <thead><tr><th>Country and survey size</th><th class="num">Survey alone</th><th class="num">With the chatbot kind</th><th class="num">With record citizens</th></tr></thead>\n      <tbody>\n        '
               + "\n        ".join(kind_rows) + "\n      </tbody>\n    </table>\n    </div>")

LABELS = [("survey alone", "Survey alone"), ("+ chatbot kind", "With the chatbot kind"), ("+ record citizens", "With record citizens, learned from past surveys"),
          ("+ record citizens (own survey)", "With record citizens, learned from your own survey"), ("+ demographics only (own survey)", "With a demographics-only model, learned from your own survey"),
          ("+ record citizens + chatbot kind", "With record citizens and the chatbot kind together")]
one_tables = []
for tag, name in [("singapore", "Singapore"), ("us", "United States")]:
    full = {(r["config"], int(r["n"])): (float(r["median"]), float(r["mean"])) for r in csv.DictReader(open(RES / f"one_method_{tag}.csv"))}
    rows_ = [f'<tr><td>{lab}</td>' + "".join(f'<td class="num">{full[(k, n)][0]:.1f} <span class="cut">({full[(k, n)][1]:.1f})</span></td>' for n in SIZES) + "</tr>" for k, lab in LABELS]
    one_tables.append(f'<div class="wrap">\n    <table>\n      <caption>{name}: points off for a typical group (average in brackets)</caption>\n'
                      '      <thead><tr><th>Method</th>' + "".join(f'<th class="num">Survey of {n}</th>' for n in SIZES) + '</tr></thead>\n      <tbody>\n        '
                      + "\n        ".join(rows_) + "\n      </tbody>\n    </table>\n    </div>")
TABLE_ONE_METHOD = "\n    ".join(one_tables)

# standout check, Singapore, survey of 300
st = pd.read_csv(RES / "standout_cells.csv")
no = st[(st.country == "Singapore") & (st.method == "noai")].set_index(["question_id", "group"]).mae_pts.sort_values(ascending=False)
top = set(no.index[:round(len(no) / 4)])
pc = PER_CELL["singapore"]
pc = pc[pc.n == 300].copy()
pc["set"] = ["standout" if (q, g) in top else "most" for q, g in zip(pc.question_id, pc.group)]
m = pc.groupby(["set", "config"]).mae.median()
SO = {s: pct(m[(s, "survey alone")], m[(s, "+ record citizens")]) for s in ("most", "standout")}

FILL = {
    "SG_REC_300": f1(SG[("+ record citizens", 300)]), "SG_ALONE_600": f1(SG[("survey alone", 600)]), "SG_ALONE_300": f1(SG[("survey alone", 300)]),
    "US_REC_150": f1(US[("+ record citizens", 150)]), "US_ALONE_600": f1(US[("survey alone", 600)]),
    "SG_REC_300_PCT": str(pct(SG[("survey alone", 300)], SG[("+ record citizens", 300)])),
    "SG_REC_600_PCT": str(pct(SG[("survey alone", 600)], SG[("+ record citizens", 600)])),
    "SG_CHAT_600_PCT": str(pct(SG[("survey alone", 600)], SG[("+ chatbot kind", 600)])),
    "SG_OWN_150": f1(SG[("+ record citizens (own survey)", 150)]), "SG_OWN_300": f1(SG[("+ record citizens (own survey)", 300)]),
    "US_OWN_300": f1(US[("+ record citizens (own survey)", 300)]),
    "N_CHINESE": str(SMALL["CHI"][2]), "N_MALAY": str(SMALL["MAL"][2]), "N_INDIAN": str(SMALL["IND"][2]),
    "CHI_ALONE": SMALL["CHI"][0], "CHI_REC": SMALL["CHI"][1], "MAL_ALONE": SMALL["MAL"][0], "MAL_REC": SMALL["MAL"][1],
    "IND_ALONE": SMALL["IND"][0], "IND_REC": SMALL["IND"][1],
    "SG_BOTH": f1(SG[("+ record citizens", 300)]),
    "SO_TXT": (f'{SO["most"]}% less error for both' if SO["most"] == SO["standout"] else f'{SO["most"]}% less error for most groups and {SO["standout"]}% for standout groups'),
    "TABLE_SMALL": TABLE_SMALL, "TABLE_KINDS": TABLE_KINDS, "TABLE_ONE_METHOD": TABLE_ONE_METHOD,
}
assert f1(SG[("+ record citizens", 300)]) == f1(SG[("survey alone", 600)]), "the page says both are the same"
# words used in the so-what bullets, checked against the data
CHECK = {"SG chatbot 300 cut (about a sixth)": pct(SG[("survey alone", 300)], SG[("+ chatbot kind", 300)]),
         "US chatbot 300 cut (about a third)": pct(US[("survey alone", 300)], US[("+ chatbot kind", 300)]),
         "SG record 300 cut (more than a quarter)": pct(SG[("survey alone", 300)], SG[("+ record citizens", 300)]),
         "US record 300 cut (half)": pct(US[("survey alone", 300)], US[("+ record citizens", 300)])}
print("checks:", CHECK)

tokens = (HERE / "tokens.css").read_text()
body = (HERE / "body.html").read_text()
css = (HERE / "style.css").read_text()


def fill(text):
    for k, v in FILL.items():
        text = text.replace("{{" + k + "}}", v)
    assert "{{" not in text, [l for l in text.splitlines() if "{{" in l][:3]
    return text


page = (f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">\n'
        '<style>\n  /* Layout: one reading column for a busy executive. Answer first, then the one idea that explains it, then the evidence, then rules and limits. Detail folded away. */\n'
        + tokens + css + "</style>\n" + fill(body.replace("{{CHART}}", chart)))
OUT.write_text(page)
print("written", OUT, len(page))
