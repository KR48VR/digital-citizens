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
import re
import pandas as pd
RES = HERE.parents[3] / "docs" / "results" / "stress_test"
SIZES = (150, 300, 600)
BOTH = "+ record citizens (own survey) + chatbot kind"
TAGS = ("singapore", "us")


def load(tag):
    out = {}
    for r in csv.DictReader(open(RES / f"one_method_{tag}.csv")):
        out[(r["config"], int(r["n"]))] = {k: float(r[k]) for k in ("median", "mean", "low", "high")}
    return out


M = {t: load(t) for t in TAGS}


def med(tag, config, n):
    return M[tag][(config, n)]["median"]


def f1(v):
    return f"{v:.1f}"


def pct(base, v):
    return round(100 * (base - v) / base)


def cut_txt(p):
    return f"{p}% less error" if p >= 0 else f"{-p}% more error"


# ---- chart: survey alone vs survey + AI (brand-new question), points off by survey size
SERIES = [("survey alone", "Survey alone", "var(--muted)"), (BOTH, "Survey + AI", "var(--s1)")]


def panel(country, tag, ymax=7.0):
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
        pts = [(xs[n], y(med(tag, key, n))) for n in SIZES]
        g.append(f'<polyline class="ln" points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" stroke="{colour}"/>')
        for n, (a, b) in zip(SIZES, pts):
            g.append(f'<circle class="pt" cx="{a:.1f}" cy="{b:.1f}" r="4.5" fill="{colour}" tabindex="0" '
                     f'data-tip="{country}, survey of {n}, {label.lower()}: {f1(med(tag, key, n))} points off"/>')
        ends.append([pts[-1][1], label, colour])
    ends.sort(key=lambda e: e[0])
    orig = [e[0] for e in ends]
    for i in range(1, len(ends)):
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + 15)
    shift = sum(orig) / len(orig) - sum(e[0] for e in ends) / len(ends)
    for (yy, label, colour), y0 in zip(ends, orig):
        yy = yy + shift
        g.append(f'<line class="key" x1="{PR+8}" y1="{y0:.1f}" x2="{PR+14}" y2="{yy:.1f}" stroke="{colour}"/>'
                 f'<line class="key" x1="{PR+14}" y1="{yy:.1f}" x2="{PR+24}" y2="{yy:.1f}" stroke="{colour}"/>'
                 f'<text class="end" x="{PR+28}" y="{yy+4:.1f}">{label}</text>')
    aria = f"{country}, brand-new question: points off for a typical group by survey size. " + " ".join(
        f"{label}: " + ", ".join(f"{f1(med(tag, key, n))} at {n}" for n in SIZES) + "." for key, label, _ in SERIES)
    return (f'<div class="panel"><p class="ptitle">{country}</p><svg class="lines" viewBox="0 0 {W} {PB+42}" role="img" aria-label="{aria}">'
            + "".join(g) + "</svg></div>")


chart = '<div class="panels">' + panel("Singapore", "singapore") + panel("United States", "us") + "</div>"

# ---- the decision table: survey of 300, what to add
def cell(tag, config, n=300, base=True):
    if (config, n) not in M[tag]:
        return '<td class="num"><span class="cut">not tested</span></td>'
    v = med(tag, config, n)
    sub = "starting point" if config == "survey alone" else cut_txt(pct(med(tag, "survey alone", n), v))
    if config == "+ last round's answers":
        sub = "about the same with no new survey"
        assert abs(med(tag, "last round's answers alone, no survey", n) - v) < 0.1
    return f'<td class="num"><b>{f1(v)}</b><span class="cut">{sub}</span></td>'


route_rows = [
    ("", "Nothing: the survey of 300 alone", "survey alone"),
    ("If your question is brand new", "The chatbot kind", "+ chatbot kind"),
    ("If your question is brand new", "Record citizens learned from your survey", "+ record citizens (own survey)"),
    ("If your question is brand new", "Both of the above", BOTH),
    ("If it was asked in other countries", "Record citizens learned from those countries", "+ record citizens"),
    ("If it was asked recently in the same survey", "Last round's answers to the same question", "+ last round's answers"),
]
rows_html = []
for q_, add, cfg in route_rows:
    sg = cell("singapore", cfg)
    us = cell("us", cfg) if cfg != "+ record citizens" else '<td class="num"><span class="cut">not tested</span></td>'
    if cfg == "+ last round's answers":
        sg = '<td class="num"><span class="cut">not tested</span></td>'
    label = f'{add}<span class="cut">{q_}</span>' if q_ else add
    rows_html.append(f"<tr><td>{label}</td>{sg}{us}</tr>")
ref = [f'<td class="num"><b>{f1(med(t, "survey alone", 600))}</b><span class="cut">for comparison</span></td>' for t in TAGS]
rows_html.append(f'<tr><td>A survey of 600 alone, no AI</td>{"".join(ref)}</tr>')
TABLE_ROUTES = ('<div class="wrap">\n    <table class="pts">\n      <caption>Points off for a typical group with a survey of 300, and how much less error than the survey alone</caption>\n'
                '      <thead><tr><th>What you add to the survey</th><th class="num">Singapore</th><th class="num">United States</th></tr></thead>\n      <tbody>\n        '
                + "\n        ".join(rows_html) + "\n      </tbody>\n    </table>\n    </div>")

# ---- small groups, Singapore, survey of 150, brand-new question
CELLS = pd.read_csv(RES / "one_method_singapore_cells.csv")
PC = CELLS.groupby(["config", "n", "question_id", "group"], as_index=False).agg(mae=("mae_pts", "mean"), ng=("n_group", "mean"))
GROUPS = {"CHI": ("ethnic=Chinese", "Chinese Singaporeans"), "MAL": ("ethnic=Malay", "Malay Singaporeans"), "IND": ("ethnic=Indian", "Indian Singaporeans")}


def grp(key, config, n=150):
    v = PC[(PC.n == n) & (PC.group == GROUPS[key][0]) & (PC.config == config)]
    return v.mae.median(), v.ng.mean()


small_rows = []
for key, (g, label) in GROUPS.items():
    a_, ng = grp(key, "survey alone")
    b_, _ = grp(key, BOTH)
    small_rows.append(f'<tr><td>{label}</td><td class="num">about {round(ng)}</td><td class="num"><b>{f1(a_)}</b></td><td class="num"><b>{f1(b_)}</b></td></tr>')
TABLE_SMALL = ('<div class="wrap">\n    <table class="pts">\n      <caption>Points off for each group, from a 150-person survey in Singapore, brand-new question</caption>\n'
               '      <thead><tr><th>Group</th><th class="num">People in the survey</th><th class="num">Survey alone</th><th class="num">With AI</th></tr></thead>\n      <tbody>\n        '
               + "\n        ".join(small_rows) + "\n      </tbody>\n    </table>\n    </div>")

# ---- analysts: every method, both countries
LABELS = [("survey alone", "Survey alone"), ("+ chatbot kind", "With the chatbot kind"),
          ("+ record citizens (own survey)", "With record citizens learned from your own survey"), (BOTH, "With record citizens from your own survey plus the chatbot kind"),
          ("+ record citizens", "With record citizens learned from past surveys"),
          ("+ record citizens + chatbot kind", "With record citizens from past surveys and the chatbot kind"),
          ("+ last round's answers", "With last round's answers to the same question"),
          ("+ demographics only (own survey)", "With a demographics-only model learned from your own survey"),
          ("+ record citizens (own survey, 20 standard questions)", "With record citizens learned from your own survey, 20 standard questions"),
          ("+ chatbot (Opus)", "With the best single chatbot in our tests (Opus)"),
          ("+ chatbot panel, averaged", "With five chatbots, simple average"),
          ("+ chatbot panel, each weighted", "With five chatbots, each counted by how accurate it had been"),
          ("chatbot kind alone, no survey", "Chatbot kind alone, no survey"), ("record citizens alone, no survey", "Record citizens from past surveys alone, no survey"),
          ("last round's answers alone, no survey", "Last round's answers alone, no survey")]
one_tables = []
for tag, name in [("singapore", "Singapore"), ("us", "United States")]:
    rows_ = []
    for k, lab in LABELS:
        if (k, 150) not in M[tag]:
            continue
        rows_.append(f'<tr><td>{lab}</td>' + "".join(f'<td class="num">{M[tag][(k, n)]["median"]:.1f} <span class="cut">({M[tag][(k, n)]["mean"]:.1f})</span></td>' for n in SIZES) + "</tr>")
    one_tables.append(f'<div class="wrap">\n    <table>\n      <caption>{name}: points off for a typical group (average in brackets)</caption>\n'
                      '      <thead><tr><th>Method</th>' + "".join(f'<th class="num">Survey of {n}</th>' for n in SIZES) + '</tr></thead>\n      <tbody>\n        '
                      + "\n        ".join(rows_) + "\n      </tbody>\n    </table>\n    </div>")
TABLE_ONE_METHOD = "\n    ".join(one_tables)

NAMES = dict(LABELS)
cmp_rows = []
for tag, name in [("singapore", "Singapore"), ("us", "United States")]:
    for r in csv.DictReader(open(RES / f"one_method_{tag}_comparisons.csv")):
        if r["a"] not in NAMES or r["b"] not in NAMES:  # later experiments (panel, short question sets) are reported elsewhere
            continue
        a = NAMES[r["a"]].replace("With ", "").replace("with ", "")
        b = NAMES[r["b"]].replace("With ", "").replace("with ", "")
        cmp_rows.append(f'<tr><td>{name}<span class="cut">{a[0].upper() + a[1:]}, {r["n_a"]} people, against {b[0].lower() + b[1:]}, {r["n_b"]} people</span></td>'
                        f'<td class="num">{float(r["difference"]):+.2f}</td><td class="num">{float(r["low"]):+.2f} to {float(r["high"]):+.2f}</td></tr>')
TABLE_COMPARE = ('<div class="wrap">\n    <table>\n      <caption class="sr">Key comparisons with 95% ranges</caption>\n'
                 '      <thead><tr><th>Comparison</th><th class="num">Difference</th><th class="num">95% range</th></tr></thead>\n      <tbody>\n        '
                 + "\n        ".join(cmp_rows) + "\n      </tbody>\n    </table>\n    </div>")

# ---- standout check (Singapore, 300, record citizens from other countries)
st = pd.read_csv(RES / "standout_cells.csv")
no = st[(st.country == "Singapore") & (st.method == "noai")].set_index(["question_id", "group"]).mae_pts.sort_values(ascending=False)
top = set(no.index[:round(len(no) / 4)])
pc3 = PC[PC.n == 300].copy()
pc3["set"] = ["standout" if (q, g) in top else "most" for q, g in zip(pc3.question_id, pc3.group)]
mm = pc3.groupby(["set", "config"]).mae.median()
SO = {s_: pct(mm[(s_, "survey alone")], mm[(s_, "+ record citizens")]) for s_ in ("most", "standout")}

FILL = {"TABLE_ROUTES": TABLE_ROUTES, "TABLE_SMALL": TABLE_SMALL, "TABLE_ONE_METHOD": TABLE_ONE_METHOD, "TABLE_COMPARE": TABLE_COMPARE,
        "SO_TXT": (f'{SO["most"]}% less error for both' if SO["most"] == SO["standout"] else f'{SO["most"]}% less error for most groups and {SO["standout"]}% for standout groups')}


FLOOR = {}
for line in (RES / "yardstick_noise.md").read_text().splitlines():
    if line.startswith("| Singapore") or line.startswith("| United States"):
        cells_ = [c.strip() for c in line.strip("|").split("|")]
        FLOOR["singapore" if cells_[0] == "Singapore" else "us"] = float(cells_[1])
WORTH = {}
for t in TAGS:
    m_ = re.search(r"^\| \+ chatbot kind \| 300 \| ([0-9.]+) \|", (RES / f"one_method_{t}.md").read_text(), flags=re.M)
    WORTH[t] = float(m_.group(1))


def inline(m):
    kind, args = m.group(1), m.group(2).split("|")
    if kind == "floor":
        return f1(FLOOR[args[0]])
    if kind == "worth":
        return str(round(WORTH[args[0]]))
    if kind == "v":
        return f1(med(args[0], args[1], int(args[2])))
    if kind == "pct":
        return str(pct(med(args[0], "survey alone", int(args[2])), med(args[0], args[1], int(args[2]))))
    if kind == "ppl":
        return str(round(grp(args[0], "survey alone")[1]))
    if kind == "grp":
        return f1(grp(args[0], args[1])[0])
    raise KeyError(kind)


# claims made in words, checked against the data
sg, us = "singapore", "us"
for n in SIZES:
    for t in TAGS:
        assert med(t, BOTH, n) < min(med(t, "+ chatbot kind", n), med(t, "+ record citizens (own survey)", n)), ("both best", t, n)
assert f1(med(sg, BOTH, 300)) == f1(med(sg, "survey alone", 600)) == f1(med(sg, "+ record citizens", 300)), "Singapore: both 2.7"
assert med(us, BOTH, 300) < med(us, "survey alone", 600)
for t in TAGS:  # rule 2: a panel does about as well as the best single chatbot; a simple average does worse than the chatbot kind
    assert abs(med(t, "+ chatbot panel, each weighted", 300) - med(t, "+ chatbot (Opus)", 300)) < 0.1, t
    assert med(t, "+ chatbot panel, averaged", 300) > med(t, "+ chatbot kind", 300), t
# rule 1: 20 standard questions almost as good as all of them in Singapore (within 0.15 points)
assert med(sg, "+ record citizens (own survey, 20 standard questions)", 300) - med(sg, "+ record citizens (own survey)", 300) < 0.15
assert pct(med(us, "survey alone", 300), med(us, "+ chatbot kind", 300)) > pct(med(sg, "survey alone", 300), med(sg, "+ chatbot kind", 300))
CHECK = {"SG chatbot vs own RC, 300 (about the same)": (f1(med(sg, "+ chatbot kind", 300)), f1(med(sg, "+ record citizens (own survey)", 300))),
         "US chatbot vs own RC, 300 (about the same)": (f1(med(us, "+ chatbot kind", 300)), f1(med(us, "+ record citizens (own survey)", 300))),
         "SG RC past vs + chatbot (adds nothing)": (f1(med(sg, "+ record citizens", 300)), f1(med(sg, "+ record citizens + chatbot kind", 300))),
         "US last round vs best (as accurate as anything)": (f1(med(us, "+ last round's answers", 300)), f1(med(us, "+ record citizens", 300)), f1(med(us, BOTH, 300)))}
print("checks:", CHECK)

tokens = (HERE / "tokens.css").read_text()
body = (HERE / "body.html").read_text()
css = (HERE / "style.css").read_text()


def fill(text):
    for k, v in FILL.items():
        text = text.replace("{{" + k + "}}", v)
    text = re.sub(r"\{\{(v|pct|ppl|grp|floor|worth):([^}]+)\}\}", inline, text)
    assert "{{" not in text, [l for l in text.splitlines() if "{{" in l][:3]
    return text


page = (f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">\n'
        '<style>\n  /* Layout: one reading column for a busy executive. Answer first, then the one idea that explains it, then the evidence, then rules and limits. Detail folded away. */\n'
        + tokens + css + "</style>\n" + fill(body.replace("{{CHART}}", chart)))
OUT.write_text(page)
print("written", OUT, len(page))
