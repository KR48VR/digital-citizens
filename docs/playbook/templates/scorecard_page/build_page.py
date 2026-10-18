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
import json
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
SERIES = [("survey alone", "Survey alone", "var(--muted)"), (BOTH, "Survey + both kinds of AI", "var(--s1)")]


def end_label(label, x):
    """Long line labels go on two lines ("Survey +" / "both kinds of AI") so they fit a phone-width chart."""
    if " + " not in label:
        return label
    first, rest = label.split(" + ", 1)
    return f'<tspan x="{x}">{first} +</tspan><tspan x="{x}" dy="1.15em">{rest}</tspan>'


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
        above = key == "survey alone"  # survey alone is the higher line at every size (asserted below)
        for n, (a, b) in zip(SIZES, pts):
            g.append(f'<circle class="pt" cx="{a:.1f}" cy="{b:.1f}" r="4.5" fill="{colour}"/>'
                     f'<text class="vlab" x="{a:.1f}" y="{b - 9 if above else b + 17:.1f}" text-anchor="middle" aria-hidden="true">{f1(med(tag, key, n))}</text>')
        ends.append([pts[-1][1], label, colour])
    ends.sort(key=lambda e: e[0])
    orig = [e[0] for e in ends]
    for i in range(1, len(ends)):
        ends[i][0] = max(ends[i][0], ends[i - 1][0] + 18)
    shift = sum(orig) / len(orig) - sum(e[0] for e in ends) / len(ends)
    for (yy, label, colour), y0 in zip(ends, orig):
        yy = yy + shift
        g.append(f'<line class="key" x1="{PR+8}" y1="{y0:.1f}" x2="{PR+14}" y2="{yy:.1f}" stroke="{colour}"/>'
                 f'<line class="key" x1="{PR+14}" y1="{yy:.1f}" x2="{PR+24}" y2="{yy:.1f}" stroke="{colour}"/>'
                 f'<text class="end" x="{PR+28}" y="{yy+4:.1f}">' + end_label(label, PR + 28) + '</text>')
    aria = f"{country}, brand-new question: median points off by survey size. " + " ".join(
        f"{label}: " + ", ".join(f"{f1(med(tag, key, n))} at {n}" for n in SIZES) + "." for key, label, _ in SERIES)
    return (f'<div class="panel"><p class="ptitle">{country}</p><svg class="lines" viewBox="0 0 {W} {PB+42}" role="img" aria-label="{aria}">'
            + "".join(g) + "</svg></div>")


chart = '<div class="panels">' + panel("Singapore", "singapore") + panel("United States", "us") + "</div>"

# ---- the decision table: survey of 300, what to add
NOT_TESTED = '<td class="num"><b aria-hidden="true">–</b><span class="cut">not tested</span></td>'
for t in TAGS:  # chart value labels sit above the survey-alone line and below the AI line
    assert all(med(t, "survey alone", n) > med(t, BOTH, n) for n in SIZES), t


def minus(x):
    return f"{x:+.2f}".replace("-", "\u2212")


def cell(tag, config, n=300, base=True):
    if (config, n) not in M[tag]:
        return NOT_TESTED
    v = med(tag, config, n)
    sub = "starting point" if config == "survey alone" else cut_txt(pct(med(tag, "survey alone", n), v))
    if config == "+ last round's answers":
        sub += '</span><span class="cut wr">the same with no new survey'
        assert abs(med(tag, "last round's answers alone, no survey", n) - v) < 0.1
    return f'<td class="num"><b>{f1(v)}</b><span class="cut">{sub}</span></td>'


route_rows = [
    ("", "Nothing: the survey of 300 alone", "survey alone"),
    ("If your question is brand new", "The chatbot kind", "+ chatbot kind"),
    ("If your question is brand new", "Record citizens learned from your own survey", "+ record citizens (own survey)"),
    ("If your question is brand new", "Both kinds of AI", BOTH),
    ("If it was asked in other countries", "Record citizens learned from those countries", "+ record citizens"),
    ("If it was asked recently in the same survey", "Last round's answers to the same question", "+ last round's answers"),
]
rows_html = []
for q_, add, cfg in route_rows:
    sg = cell("singapore", cfg)
    us = cell("us", cfg) if cfg != "+ record citizens" else NOT_TESTED
    if cfg == "+ last round's answers":
        sg = NOT_TESTED
    label = f'{add}<span class="cut">{q_}</span>' if q_ else add
    rows_html.append(f'<tr><th scope="row">{label}</th>{sg}{us}</tr>')
ref = [f'<td class="num"><b>{f1(med(t, "survey alone", 600))}</b><span class="cut">for comparison</span></td>' for t in TAGS]
rows_html.append(f'<tr><th scope="row">Survey alone, 600 people</th>{"".join(ref)}</tr>')
TABLE_ROUTES = ('<div class="wrap">\n    <table class="pts">\n      <caption>Median points off with a survey of 300, and how much less error than the survey alone. Percentages use unrounded figures.</caption>\n'
                '      <thead><tr><th>What you add to the survey</th><th class="num">Singapore</th><th class="num">United States</th></tr></thead>\n      <tbody>\n        '
                + "\n        ".join(rows_html) + "\n      </tbody>\n    </table>\n    </div>")

# ---- small groups, Singapore, survey of 150, brand-new question
CELLS = pd.read_csv(RES / "one_method_singapore_cells.csv")
PC = CELLS.groupby(["config", "n", "question_id", "group"], as_index=False).agg(mae=("mae_pts", "mean"), ng=("n_group", "mean"))
GROUPS = {"CHI": ("ethnic=Chinese", "Chinese Singaporeans"), "MAL": ("ethnic=Malay", "Malay Singaporeans"), "IND": ("ethnic=Indian", "Indian Singaporeans")}
OTHER_GROUPS = {"OLD": ("age_band=60+", "people over 60")}  # quoted in the text, not in the small-groups table


def grp(key, config, n=150):
    v = PC[(PC.n == n) & (PC.group == {**GROUPS, **OTHER_GROUPS}[key][0]) & (PC.config == config)]
    return v.mae.median(), v.ng.mean()


SMALL_N = 300  # same survey size as the rest of the page
small_rows = []
for key, (g, label) in GROUPS.items():
    a_, ng = grp(key, "survey alone", SMALL_N)
    b_, _ = grp(key, BOTH, SMALL_N)
    small_rows.append(f'<tr><th scope="row">{label}</th><td class="num">about {round(ng)}</td><td class="num"><b>{f1(a_)}</b></td><td class="num"><b>{f1(b_)}</b></td></tr>')
TABLE_SMALL = ('<div class="wrap">\n    <table class="pts">\n      <caption>Points off for each group (the median across its 20 questions), from a 300-person survey in Singapore, brand-new question. "With both kinds of AI" means the survey blended with record citizens and the chatbot.</caption>\n'
               '      <thead><tr><th>Group</th><th class="num">People in the survey</th><th class="num">Survey alone</th><th class="num">With both kinds of AI</th></tr></thead>\n      <tbody>\n        '
               + "\n        ".join(small_rows) + "\n      </tbody>\n    </table>\n    </div>")

# ---- the blend: how much each voice counts (Singapore, survey of 300, brand-new question)
def md_table(text, first_header):
    """Rows of the markdown table whose header starts with first_header, as dicts."""
    lines_ = text.splitlines()
    i = next(k for k, l in enumerate(lines_) if l.startswith(first_header))
    head = [c.strip() for c in lines_[i].strip("|").split("|")]
    out = []
    for l in lines_[i + 2:]:
        if not l.startswith("|"):
            break
        out.append(dict(zip(head, [c.strip() for c in l.strip("|").split("|")])))
    return out


SG_MD = (RES / "one_method_singapore.md").read_text()
W_ = next(r for r in md_table(SG_MD, "| config | n | chat |") if r["config"] == BOTH and r["n"] == "300")
SIZE_ = {r["group"]: float(r["300"]) for r in md_table(SG_MD, "| group | 150 |")}
BL = {"rec": float(W_["rec_own"]), "chat": float(W_["chat"])}


def shares(n_people):
    raw = [n_people, BL["rec"], BL["chat"]]
    pc = [100 * v / sum(raw) for v in raw]
    out = [int(p) for p in pc]  # largest remainder, so the three add up to 100
    for k in sorted(range(3), key=lambda k: pc[k] - out[k], reverse=True)[:100 - sum(out)]:
        out[k] += 1
    return out


BLEND = {key: (SIZE_[GROUPS[key][0]], shares(SIZE_[GROUPS[key][0]])) for key in ("IND", "CHI")}
EXAMPLE = (BLEND["IND"][0] * 40 + BL["rec"] * 50 + BL["chat"] * 45) / (BLEND["IND"][0] + BL["rec"] + BL["chat"])
assert BLEND["IND"][1][0] < BLEND["CHI"][1][0] and abs(EXAMPLE - 50) < abs(EXAMPLE - 45) < abs(EXAMPLE - 40)
SEG = [("sv", "Survey"), ("rc", "Record citizens"), ("cb", "Chatbot")]
bars = []
for key in ("IND", "CHI"):
    n_, sh = BLEND[key]
    segs = "".join(f'<span class="seg {c}" style="flex:{v} 1 0">{f"{v}%" if v >= 12 else ""}</span>' for (c, _), v in zip(SEG, sh))
    key_ = "".join(f'<span><i class="sw {c}"></i>{lab} {v}%</span>' for (c, lab), v in zip(SEG, sh))
    bars.append(f'<div class="brow"><p class="blab"><strong>{GROUPS[key][1]}</strong> · about {round(n_)} people in the survey</p>'
                f'<div class="bar" aria-hidden="true">{segs}</div><p class="bkey">{key_}</p></div>')
BLEND_BARS = ('<figure class="blendfig"><h3>How much each voice counts</h3><p class="howto">Singapore, survey of 300, brand-new question.</p>'
              + "".join(bars) + "</figure>")
_n, _r, _c = round(BLEND["IND"][0]), round(BL["rec"]), round(BL["chat"])  # the example's working uses the rounded numbers it shows
assert round((_n * 40 + _r * 50 + _c * 45) / (_n + _r + _c)) == round(EXAMPLE)
BLEND_TXT = {"rec": str(_r), "chat": str(_c), "IND_n": str(_n), "total": str(_n + _r + _c), "example": str(round(EXAMPLE))}


# ---- decision tree: how much AI adds by group size (both countries, every survey size)
GS = []
for t in TAGS:
    c_ = pd.read_csv(RES / f"one_method_{t}_cells.csv")
    pc_ = c_.groupby(["config", "n", "question_id", "group"], as_index=False).agg(mae=("mae_pts", "mean"), ng=("n_group", "mean"))
    for (n, g), d in pc_[pc_.config.isin(["survey alone", BOTH])].groupby(["n", "group"]):
        a_, b_ = d[d.config == "survey alone"].mae.median(), d[d.config == BOTH].mae.median()
        GS.append((d.ng.mean(), a_ - b_, 1 - b_ / a_))
GS = pd.DataFrame(GS, columns=["people", "gain", "cut"])
SMALL, LARGE = GS[GS.people < 100], GS[GS.people >= 100]
TREE = {"gain_small": f1(SMALL.gain.median()), "pct_small": str(round(100 * SMALL.cut.median())),
        "gain_large": f1(LARGE.gain.median()), "pct_large": str(round(100 * LARGE.cut.median()))}
assert SMALL.gain.median() > 3 * LARGE.gain.median(), "AI adds most below about 100 people"

# ---- boosting small groups (rule 3, evidence map): about a point without AI, little with it
BOOST = {}
for line in (RES / "boost_vs_standard.md").read_text().splitlines():
    m_ = re.match(r"\| ethnic=(Malay|Indian) \| (.+?) \| [0-9.]+ \| [0-9.]+ \| ([+-][0-9.]+) \(([+-][0-9.]+) to ([+-][0-9.]+)\)", line)
    if m_:
        BOOST[(m_.group(1), m_.group(2))] = tuple(float(x) for x in m_.groups()[2:])
for g in ("Malay", "Indian"):
    assert -1.5 < BOOST[(g, "survey alone")][0] < -0.75, g
    assert BOOST[(g, BOTH)][0] > -0.6 and BOOST[(g, BOTH)][2] > 0, g


# ---- the two cases from the short answer, side by side (Singapore, survey of 300, median over groups and questions)
# Same five rows in both cases, in the same order, so they line up across the two columns.
def case_rows(rows, top):
    return "".join(f'<div class="crow {cls}"><span class="cl">{label}</span><span class="ct" aria-hidden="true"><i style="width:{100 * v / top:.0f}%"></i></span><b>{f1(v)}<span class="sr"> points off</span></b></div>'
                   for label, cls, v in rows)


sg_alone, sg_600 = med("singapore", "survey alone", 300), med("singapore", "survey alone", 600)
sg_chat, sg_past = med("singapore", "+ chatbot kind", 300), med("singapore", "+ record citizens", 300)
sg_past_both = med("singapore", "+ record citizens + chatbot kind", 300)
sg_own, sg_both = med("singapore", "+ record citizens (own survey)", 300), med("singapore", BOTH, 300)
assert sg_past < sg_chat and f1(sg_past) == f1(sg_600), "case 1: record citizens beat the chatbot and match 600"
assert abs(sg_past_both - sg_past) < 0.1, "case 1: adding the chatbot to record citizens did not help"
assert sg_both < min(sg_chat, sg_own) and f1(sg_both) == f1(sg_600), "case 2: both kinds best and match 600"
TOP = max(sg_alone, sg_600)
CASES = ('<div class="cases">'
         '<div class="case"><h3>1. Your question was already asked in large surveys</h3><div class="chead" aria-hidden="true">points off</div>'
         + case_rows([("Survey of 300 alone", "c-sv", sg_alone), ("Blended with the chatbot", "c-cb", sg_chat),
                      ("Blended with record citizens learned from other countries", "c-rc", sg_past),
                      ("Blended with both kinds of AI", "c-both", sg_past_both), ("Survey of 600 alone, for comparison", "c-ref", sg_600)], TOP)
         + '<p><strong>Record citizens beat the chatbot,</strong> and adding the chatbot to them did not help. They matched a survey twice the size.</p></div>'
         '<div class="case"><h3>2. Your question is brand new</h3><div class="chead" aria-hidden="true">points off</div>'
         + case_rows([("Survey of 300 alone", "c-sv", sg_alone), ("Blended with the chatbot", "c-cb", sg_chat),
                      ("Blended with record citizens learned from your survey", "c-rc", sg_own),
                      ("Blended with both kinds of AI", "c-both", sg_both), ("Survey of 600 alone, for comparison", "c-ref", sg_600)], TOP)
         + '<p><strong>The two kinds did about as well as each other;</strong> blended in together, they matched a survey twice the size.</p></div>'
         '</div>')


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
        rows_.append(f'<tr><th scope="row">{lab}</th>' + "".join(f'<td class="num">{M[tag][(k, n)]["median"]:.1f} <span class="cut">({M[tag][(k, n)]["mean"]:.1f})</span></td>' for n in SIZES) + "</tr>")
    one_tables.append(f'<div class="wrap">\n    <table>\n      <caption>{name}: median points off (average in brackets)</caption>\n'
                      '      <thead><tr><th>Method</th>' + "".join(f'<th class="num">Survey of {n}</th>' for n in SIZES) + '</tr></thead>\n      <tbody>\n        '
                      + "\n        ".join(rows_) + "\n      </tbody>\n    </table>\n    </div>")
TABLE_ONE_METHOD = "\n    ".join(one_tables)

NAMES = dict(LABELS)
cmp_tables = []
for tag, name in [("singapore", "Singapore"), ("us", "United States")]:
    cmp_rows = []
    for r in csv.DictReader(open(RES / f"one_method_{tag}_comparisons.csv")):
        if r["a"] not in NAMES or r["b"] not in NAMES:  # later experiments (panel, short question sets) are reported elsewhere
            continue
        a = NAMES[r["a"]].replace("With ", "").replace("with ", "")
        b = NAMES[r["b"]].replace("With ", "").replace("with ", "")
        cmp_rows.append(f'<tr><th scope="row">{a[0].upper() + a[1:]}, {r["n_a"]} people, against {b[0].lower() + b[1:]}, {r["n_b"]} people</th>'
                        f'<td class="num">{minus(float(r["difference"]))}</td><td class="num"><span class="nw">{minus(float(r["low"]))} to {minus(float(r["high"]))}</span></td></tr>')
    cmp_tables.append(f'<div class="wrap">\n    <table>\n      <caption>{name}: key comparisons, with 95% ranges</caption>\n'
                      '      <thead><tr><th>Comparison</th><th class="num">Difference</th><th class="num">95% range</th></tr></thead>\n      <tbody>\n        '
                      + "\n        ".join(cmp_rows) + "\n      </tbody>\n    </table>\n    </div>")
TABLE_COMPARE = "\n    ".join(cmp_tables)

# ---- standout check (Singapore, 300, record citizens from other countries)
st = pd.read_csv(RES / "standout_cells.csv")
no = st[(st.country == "Singapore") & (st.method == "noai")].set_index(["question_id", "group"]).mae_pts.sort_values(ascending=False)
top = set(no.index[:round(len(no) / 4)])
pc3 = PC[PC.n == 300].copy()
pc3["set"] = ["standout" if (q, g) in top else "most" for q, g in zip(pc3.question_id, pc3.group)]
mm = pc3.groupby(["set", "config"]).mae.median()
SO = {s_: pct(mm[(s_, "survey alone")], mm[(s_, "+ record citizens")]) for s_ in ("most", "standout")}

FILL = {"CASES": CASES, "BLEND_BARS": BLEND_BARS, "TABLE_ROUTES": TABLE_ROUTES, "TABLE_SMALL": TABLE_SMALL, "TABLE_ONE_METHOD": TABLE_ONE_METHOD, "TABLE_COMPARE": TABLE_COMPARE,
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


SELF = json.load(open(RES.parent / "self_agreement_twin2k.json"))  # same people asked twice (scripts/self_agreement_twin2k.py)
SELF_FMT = {"match": lambda d: str(round(100 * d["match"])), "match_yes_no": lambda d: str(round(100 * d["match_yes_no"])),
            "match_6_7": lambda d: str(round(100 * d["match_6_7_options"])), "shift_everyone": lambda d: f1(d["shift_everyone"]),
            "shift_group": lambda d: f1(d["shift_typical_group"]), "questions": lambda d: str(d["questions"]),
            "people": lambda d: f"{d['people']:,}"}


def inline(m):
    kind, args = m.group(1), m.group(2).split("|")
    if kind == "tree":
        return TREE[args[0]]
    if kind == "blend":
        return BLEND_TXT[args[0]]
    if kind == "self":
        return SELF_FMT[args[0]](SELF)
    if kind == "floor":
        return f1(FLOOR[args[0]])
    if kind == "worth":
        return str(round(WORTH[args[0]]))
    if kind == "v":
        return f1(med(args[0], args[1], int(args[2])))
    if kind == "gain":  # points closer than the survey alone, from unrounded values
        return f1(med(args[0], "survey alone", int(args[2])) - med(args[0], args[1], int(args[2])))
    if kind == "pct":
        return str(pct(med(args[0], "survey alone", int(args[2])), med(args[0], args[1], int(args[2]))))
    if kind == "ppl":
        return str(round(grp(args[0], "survey alone", *(int(a) for a in args[1:]))[1]))
    if kind == "grp":
        return f1(grp(args[0], args[1], *(int(a) for a in args[2:]))[0])
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
CMP = {}
for t in TAGS:
    for r in csv.DictReader(open(RES / f"one_method_{t}_comparisons.csv")):
        CMP[(t, r["a"], r["b"], int(r["n_a"]), int(r["n_b"]))] = (float(r["low"]), float(r["high"]))
for t in TAGS:  # short answer: brand new, the two kinds about as good as each other; asked before, record citizens beat the chatbot and adding it did not help
    for n in SIZES:
        lo, hi = CMP[(t, "+ chatbot kind", "+ record citizens (own survey)", n, n)]
        assert lo < 0 < hi, ("two kinds differ", t, n)
    lo, hi = CMP[(t, "+ record citizens + chatbot kind", "+ record citizens", 300, 300)]
    assert lo < 0 < hi, ("chatbot helped record citizens", t)
    assert med(t, "+ record citizens", 300) < med(t, "+ chatbot kind", 300), t
# worked example, step 3: Claude Opus was the best single chatbot by a small margin; the page's chatbot kind (Claude Fable 5.1) was about as good
for t in TAGS:
    singles = {k_: med(t, k_, 300) for k_ in ("+ chatbot kind", "+ chatbot (Opus)", "+ chatbot (Sonnet)", "+ chatbot (Haiku)", "+ chatbot (Qwen, open, Asian-built)")}
    assert min(singles, key=singles.get) == "+ chatbot (Opus)" and singles["+ chatbot kind"] - singles["+ chatbot (Opus)"] < 0.5, t
# the "what counts as good enough" boxes: 3 is a survey of 600 alone; 5 is a survey of 150 alone or the chatbot alone (Singapore)
assert 2.5 < med(sg, "survey alone", 600) < 3.5 and 3.5 < med(us, "survey alone", 600) < 4
for k_, n_ in (("survey alone", 150), ("chatbot kind alone, no survey", 150)):
    assert 4.5 < med(sg, k_, n_) < 5.5, k_
# 15 is splitting answers evenly across the choices, at group level (baseline tests)
for t, lo_, hi_ in (("singapore", 14.5, 15.5), ("united_states", 12.5, 14)):
    rows_ = [r_ for r_ in (RES.parent / f"baselines_wvs7_{t}.md").read_text().split("## Segment level")[1].splitlines() if r_.startswith("| uniform")]
    assert lo_ < float(rows_[0].split("|")[6]) < hi_, t
# "the changes mostly cancel out ... more for small groups"; "no AI can predict one person much better"
assert SELF["shift_typical_group"] < 2 and SELF["group_size_vs_shift_spearman"] < -0.5 and SELF["match_6_7_options"] < 0.5
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
    text = re.sub(r"\{\{(v|pct|gain|ppl|grp|floor|worth|self|blend|tree):([^}]+)\}\}", inline, text)
    assert "{{" not in text, [l for l in text.splitlines() if "{{" in l][:3]
    return text


page = (f'<title>{TITLE}</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Source+Serif+4:opsz,wght@8..60,500;8..60,600&family=IBM+Plex+Sans:wght@400;500;600&display=swap">\n'
        '<style>\n  /* Layout: one reading column for a busy executive. Answer first, then the one idea that explains it, then the evidence, then rules and limits. Detail folded away. */\n'
        + tokens + css + "</style>\n" + fill(body.replace("{{CHART}}", chart)))
OUT.write_text(page)
print("written", OUT, len(page))
