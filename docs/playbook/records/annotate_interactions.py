import json, re
H = "/tmp/claude-0/-home-user-digital-citizens/9ee5706b-1ea3-5423-a58d-280007966042/scratchpad/history"
turns = json.load(open(f"{H}/turns_full.json"))
SYSTEM = {1, 2, 3, 4, 5, 6, 12, 13, 16, 17, 18}
# task id, type, what Claude did (from the transcript), optional note on who brought the idea
A = {
 0:  ("T1", "independent", "Researched the evidence and datasets with three helper agents, wrote the measurement plan and country recommendation, built the first code and ran baselines on real US data, about an hour of work before reporting back."),
 7:  ("T2", "teammate", "Agreed and changed plan: stood in for the model to make blind predictions, downloaded the World Values Survey through a headless browser instead of King's own browser, and stress-tested the US, Singapore and China."),
 8:  ("T3", "independent", "Tested five remedies on my own; three failed, and anchoring each citizen to a real survey record worked (Singapore group differences reproduced 52% vs 36%)."),
 9:  ("T4", "tool", "Re-explained with an everyday analogy: the AI gives an 'average Singaporean' answer to every group."),
 10: ("T5", "independent", "Built the first scorecard page and downloaded all 62 World Values Survey countries in the background, then trained record citizens on 61 of them."),
 11: ("T5", "teammate", "Took up King's idea mid-task: built a pooling layer that weights each source by its track record, the 'superforecasting' approach King described."),
 14: ("T4", "tool", "Explained the pooling results simply."),
 15: ("T6", "teammate", "Took up King's challenge: two helper agents combed news, polls and reports; 96 published Singapore findings were turned into evidence and tested. Result: worth about 1% of face value."),
 19: ("T4", "tool", "Gave the conclusion in one sentence and a short plain version."),
 20: ("T4", "tool", "Re-explained with the 'one actor playing a thousand roles' picture."),
 21: ("T4", "tool", "Explained 'spreading' with a 300-person survey example."),
 22: ("T7", "teammate", "Built on King's library idea: set out three conditions for it to work, then offered to test it."),
 23: ("T7", "independent", "Designed and ran the library test on two US surveys (about 50 actions, a 26-minute background run); found and corrected my own earlier error in scoring small surveys."),
 24: ("T4", "tool", "Cut the library findings down to three parts: search works, borrowing numbers does not, filling in groups works."),
 25: ("T8", "tool", "Built a summary table of every technique and its points off."),
 26: ("T8", "teammate", "Rebuilt the table around King's suggestion: the one-line summary became the spine of the table."),
 27: ("T8", "tool", "Defined 'points off' and 'group differences captured' with worked examples."),
 28: ("T8", "teammate", "Confirmed King's business reading (smaller or more frequent surveys) and added four cautions, including that the overall number does not improve."),
 29: ("T8", "tool", "Replaced my jargon: 'spread' became 'fill in the groups', 'headline number' became 'the overall number'."),
 30: ("T9", "teammate", "King's question surfaced the key distinction: the chatbot kind versus the pattern-finding kind built on real records."),
 31: ("T9", "tool", "Put the one-liner, the story table and the two-kinds explanation on the page."),
 32: ("T10", "tool", "Reviewed the page, found it said the same thing four ways, and rebuilt it around what AI can and cannot do."),
 33: ("T10", "tool", "Rewrote the two-kinds box around one example person, a 62-year-old woman."),
 34: ("T9", "teammate", "Confirmed King's reading and refined it: her record holds her answers to other questions, not to the new one."),
 35: ("T9", "teammate", "Added the two-women example and a chart showing the chatbot reproduces 81% of group differences in the US against 36% in Singapore."),
 36: ("T11", "teammate", "Reframed against the no-AI baseline: the chatbot's real contribution in Singapore was 0.2 points; conceded 'barely helped' was too harsh for standout groups."),
 37: ("T11", "teammate", "Explained the gap honestly, then ran the missing US test: record citizens beat the chatbot in the US too (1.8 vs 2.3 points)."),
 38: ("T12", "tool", "Rewrote the one-line result to open with the role of AI."),
 39: ("T12", "teammate", "Added how AI learns across 61 countries, with the 2-vs-61 evidence, and flagged cities as untested."),
 40: ("T12", "tool", "Stacked the 'helps / does not help' lists so they no longer line up under the two kinds of AI."),
 41: ("T12", "tool", "Explained 'typical' and 'big misses' under the table."),
 42: ("T12", "tool", "Replaced the statistics with a commute comparison."),
 43: ("T12", "teammate", "Rewrote the explanation through the 62-year-old woman, as King suggested, so readers meet one person throughout."),
 44: ("T12", "tool", "Proposed 'standout groups' and 'most groups' and applied them everywhere."),
 45: ("T13", "teammate", "Corrected King's reading: the first column is no AI at all; showed the share of error each kind removes."),
 46: ("T13", "tool", "Proposed reframing around 'how much error AI removes' with a chart and three takeaways."),
 47: ("T13", "teammate", "Confirmed King's summary with one refinement: the chatbot catches up for standout groups."),
 48: ("T13", "tool", "Turned the findings into a 'when to use which' guide."),
 49: ("T13", "tool", "Reduced the guide to three steps and one 'don't'."),
 50: ("T13", "teammate", "Adopted King's principle: re-wrote the guide in the page's agreed terms only."),
 51: ("T14", "teammate", "Admitted the claim was untested, removed it from the page, and added error-reduction figures to every step."),
 52: ("T15", "tool", "Rebuilt the whole page as a C-suite guide: four rules, what it is worth, two kinds of AI, one chart."),
 53: ("T15", "teammate", "Re-ordered the page so every term is defined before use, and replaced 'closest question' with a plain rule."),
 54: ("T15", "teammate", "Kept King's wording and fixed two small things: 'stretches' and a shorter phrase for the chatbot."),
 55: ("T15", "teammate", "Split the short answer into three paragraphs as King drafted, and named the chatbot kind too for symmetry."),
 56: ("T15", "teammate", "Explained the 90,000, and surfaced a bigger gap: a new product question is never asked abroad, so the AI must learn from King's own survey, which needs standard questions."),
 57: ("T15", "tool", "Merged two paragraphs and moved 'what it is worth' after the definitions."),
 58: ("T15", "tool", "Cut the 'worth' section to the comparison box only and moved the points explanation later."),
 59: ("T15", "tool", "Rebuilt the middle of the page into worth, how we measure, then points to error removed, as King laid out."),
 60: ("T15", "tool", "Named both sides of the box and tied the table intro to the short answer; changed 'simplest option' to 'no AI'."),
 61: ("T15", "teammate", "Agreed, and pointed out that 'small groups' and 'standout groups' are two different ideas; built the section in three steps."),
 62: ("T15", "tool", "Explained the footnote and folded it into one plain sentence."),
 63: ("T14", "teammate", "Checked the data: people over 60 were the most distinctive group on 0 of 20 questions; replaced with Malay Singaporeans and young adults."),
 64: ("T15", "tool", "Rewrote the two identical bullets to say how each kind of AI differs."),
 65: ("T15", "tool", "Moved the 'reading a cell' note to before the table."),
 66: ("T15", "teammate", "Made the standout-groups point general with test examples, and capitalised 'No AI' wherever it names the column."),
 67: ("T16", "teammate", "Reviewed each rule against what we had learned and proposed revisions and a new heading."),
 68: ("T16", "tool", "Wrote the five rules as King specified, checking each number (published findings made estimates slightly worse)."),
 69: ("T16", "teammate", "Recommended keeping the limits after the rules, folded in the pilot step, and added the three-countries limit."),
 70: ("T16", "teammate", "Proposed 'Limits, and areas for further experimentation' and a split-sample pilot instead of 'check against a larger survey'."),
 71: ("T16", "tool", "Applied the agreed wording."),
 72: ("T14", "teammate", "Traced the figure to the World Values Survey file and recomputed it; reworded the pilot around '300 + record citizens = 600'."),
 73: ("T14", "teammate", "Found the fieldwork dates (Nov 2019 to Mar 2020) via the Institute of Policy Studies and put them on the page."),
 74: ("T14", "teammate", "Checked what each method was asked: record citizens are tied to that survey window, the chatbot to no date at all."),
 75: ("T16", "tool", "Replaced the example with a short plain statement."),
 76: ("T17", "independent", "Running a full QA pass with an independent helper agent, then writing this record and the reusable package."),
}
TASKS = {
 "T1": ("Set the goal and build the first version", "King"),
 "T2": ("Stress-test the chatbot on public data", "King"),
 "T3": ("Fix the flattening problem", "King"),
 "T4": ("Explain the findings in plain language", "King"),
 "T5": ("Add more data and weigh sources by track record", "King"),
 "T6": ("Test news, polls and reports as evidence", "King"),
 "T7": ("Test the survey-library idea", "King"),
 "T8": ("Summarise every technique in one table", "King"),
 "T9": ("Separate the two kinds of AI", "King"),
 "T10": ("Streamline the scorecard page", "King"),
 "T11": ("Compare the United States with Singapore", "King"),
 "T12": ("Polish the page's language", "King"),
 "T13": ("Turn findings into guidance", "King"),
 "T14": ("Fact-check claims on the page", "King"),
 "T15": ("Rebuild the page for a C-suite reader", "King"),
 "T16": ("Write the five rules and the limits", "King"),
 "T17": ("QA and documentation", "King"),
}
rows = []
for i, t in enumerate(turns):
    if i in SYSTEM: continue
    assert i in A, i
    task, typ, did = A[i]
    k = re.sub(r"\s+", " ", t["king"]).replace("[mid-task]", "").strip()
    shot = "[screenshot]" in k
    k = k.replace("[screenshot]", "").strip()
    words = k.split(" ")
    quote = " ".join(words[:28]) + (" …" if len(words) > 28 else "")
    rows.append({"n": len(rows) + 1, "time": t["ts"][11:16], "task": task, "type": typ, "king": quote, "screenshot": shot,
                 "mid_task": "[mid-task]" in t["king"], "claude": did, "actions": sum(t["tools"].values())})
json.dump({"rows": rows, "tasks": TASKS}, open(f"{H}/interactions.json", "w"), indent=1)
from collections import Counter
c = Counter(r["type"] for r in rows); print(len(rows), c)
print("screenshots", sum(r["screenshot"] for r in rows), "mid-task", sum(r["mid_task"] for r in rows))
bt = {}
for r in rows: bt.setdefault(r["task"], Counter())[r["type"]] += 1
for k in TASKS: print(k, TASKS[k][0], dict(bt.get(k, {})))
