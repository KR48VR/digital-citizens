"""Build the Digital Citizens Casebook page from template.html, facts.json and the records folder."""
import json, html
from collections import Counter
from pathlib import Path
HERE = Path(__file__).resolve().parent
REC = HERE.parents[1] / "records"
D = json.load(open(REC / "interactions.json"))
rows, TASKS = D["rows"], D["tasks"]
QA = json.load(open(REC / "qa_log.json"))
FACTS = json.load(open(HERE / "facts.json"))
e = html.escape
TYPE_LABEL = {"tool": "Tool", "teammate": "Teammate", "independent": "Independent"}
cnt = Counter(r["type"] for r in rows)

# ---------- King and AI: task table
task_rows = []
for tid, (name, _) in TASKS.items():
    rs = [r for r in rows if r["task"] == tid]
    c = Counter(r["type"] for r in rs)
    t0, t1 = rs[0]["time"], rs[-1]["time"]
    kp, cp = FACTS["task_parts"][tid]
    task_rows.append(f'<tr><td class="tid">{tid[1:]}</td><td><strong>{e(name)}</strong><span class="cut">{t0 if t0 == t1 else f"{t0}–{t1}"}</span></td><td>{e(kp)}</td><td>{e(cp)}</td>'
                     f'<td class="num">{c.get("tool",0)}</td><td class="num">{c.get("teammate",0)}</td><td class="num">{c.get("independent",0)}</td></tr>')

# ---------- timeline dots (every interaction in order)
W, X0 = 700, 10
step = (W - 2 * X0 - 10) / (len(rows) - 1)
dots = []
prev_task = None
seen_tasks = set()
last_lab_x = -99
for i, r in enumerate(rows):
    x = X0 + i * step
    cls = {"tool": "d-tool", "teammate": "d-team", "independent": "d-ind"}[r["type"]]
    dots.append(f'<circle class="dot {cls}" cx="{x:.1f}" cy="30" r="4.2" tabindex="0" data-tip="#{r["n"]} {r["time"]} · {TYPE_LABEL[r["type"]]} · King: {e(r["king"][:90])}"/>')
    if r["task"] != prev_task:
        lab = ""
        if r["task"] not in seen_tasks:
            ly = 10 if x - last_lab_x >= 16 else 58  # a label too close to the previous one goes below the line
            lab = f'<text class="tl" x="{x-3:.1f}" y="{ly}">{r["task"][1:]}</text>'
            if ly == 10:
                last_lab_x = x
        dots.append(f'<line class="tick" x1="{x-5.2:.1f}" y1="14" x2="{x-5.2:.1f}" y2="46"/>{lab}')
        prev_task = r["task"]; seen_tasks.add(r["task"])
timeline = f'<svg viewBox="0 0 {W} 78" role="img" aria-label="Timeline of all {len(rows)} interactions in order, coloured by type: {cnt["tool"]} tool, {cnt["teammate"]} teammate, {cnt["independent"]} independent. Numbers mark where each task starts.">{"".join(dots)}<text class="tl" x="10" y="76">01:38</text><text class="tl" x="{W-10}" y="76" text-anchor="end">{rows[-1]["time"]}</text></svg>'

# ---------- full interaction log
log_rows = []
for r in rows:
    tag = {"tool": "t-tool", "teammate": "t-team", "independent": "t-ind"}[r["type"]]
    extra = []
    if r["screenshot"]: extra.append("with screenshot")
    if r["mid_task"]: extra.append("sent mid-task")
    ex = f'<span class="cut">{", ".join(extra)}</span>' if extra else ""
    log_rows.append(f'<tr data-type="{r["type"]}"><td class="num">{r["n"]}</td><td class="num">{r["time"]}</td><td class="task">{r["task"][1:]}</td><td><span class="tag {tag}">{TYPE_LABEL[r["type"]]}</span></td>'
                    f'<td class="q blk" data-l="King said">“{e(r["king"])}”{ex}</td><td class="blk" data-l="Claude did">{e(r["claude"])}</td></tr>')

# ---------- examples per type
def ex_block(typ):
    out = []
    for n in FACTS["examples"][typ]:
        r = rows[n - 1]
        out.append(f'<li><span class="cut">#{r["n"]}, {r["time"]}, task {r["task"][1:]}</span><span class="q">King: “{e(r["king"])}”</span><span>Claude: {e(r["claude"])}</span></li>')
    return "".join(out)

# ---------- QA log
qa_rows = []
for q in QA:
    st = q["status"]
    qa_rows.append(f'<tr><td class="num">{q["id"]}</td><td>{e(q["when"])}</td><td>{e(q["area"])}</td><td class="blk" data-l="Finding">{e(q["finding"])}</td><td class="blk" data-l="Fix">{e(q["fix"])}</td><td><span class="tag {"t-team" if st=="Fixed" else "t-tool"}">{e(st)}</span></td></tr>')
qa_counts = Counter(q["area"] for q in QA)

tpl = (HERE / "template.html").read_text()
out = (tpl.replace("{{TASK_ROWS}}", "\n".join(task_rows)).replace("{{TIMELINE}}", timeline).replace("{{LOG_ROWS}}", "\n".join(log_rows))
          .replace("{{EX_TOOL}}", ex_block("tool")).replace("{{EX_TEAM}}", ex_block("teammate")).replace("{{EX_IND}}", ex_block("independent"))
          .replace("{{QA_ROWS}}", "\n".join(qa_rows)).replace("{{N_TOOL}}", str(cnt["tool"])).replace("{{N_TEAM}}", str(cnt["teammate"]))
          .replace("{{N_IND}}", str(cnt["independent"])).replace("{{N_ALL}}", str(len(rows))).replace("{{N_QA}}", str(len(QA)))
          .replace("{{QA_AREAS}}", ", ".join(f"{v} {k.lower()}" for k, v in qa_counts.most_common())))
for k, v in FACTS["scalars"].items():
    out = out.replace("{{" + k + "}}", str(v))
assert "{{" not in out, [l for l in out.splitlines() if "{{" in l][:3]
(HERE / "casebook.html").write_text(out)
print("companion written", len(out), dict(cnt))
