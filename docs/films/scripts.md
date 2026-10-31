# Two films: scripts (as built, version 1)

Words on screen, no voice-over, original music written in code. Landscape 16:9, 24 frames a second.
Colours match the scorecard and casebook: blue = both kinds of AI blended in (Film 1) or "tool" (Film 2),
green = record citizens or "teammate", orange = the chatbot or "independent".
Sources in brackets: SC = scorecard (version 75), CB = casebook, IX = the casebook's record of King's messages
(`docs/playbook/records/interactions.json`), by message number.

---

## Film 1: "Every group heard" (1:39), plus a short cut (0:35)

For funders and government. Leads with who benefits, then the proof, then the ask. Each dot is one person.

| Time | What you see | Words on screen |
|---|---|---|
| 0:00 | Poster: a faint crowd of 300 dots, 28 of them blue | **Digital Citizens.** Hear every group, even the small ones. Built by King and Claude |
| 0:05 | 300 dots pop in, in waves on the beat | Before a policy changes, you ask people what they think. A survey of 300 Singaporeans. Each dot is one person. |
| 0:13 | The dots sort into groups; 28 light up | Most are Chinese Singaporeans. Only about 28 are Indian Singaporeans. Labels: about 231 Chinese Singaporeans, about 35 Malay, about 28 Indian, a few others [SC small groups] |
| 0:24 | The 28 gather and tremble; a marker wobbles and settles on a scale | An answer read off 28 people is shaky. In our test, their answer came out 5.6 points off what Indian Singaporeans really think. Points off: how far an answer is from what people really said, in percentage points. Scale: 1.5 best possible, 3 good enough to act on, 5 rough level only, 15 guessing blind [SC small groups; what counts as good enough] |
| 0:40 | Green dots stream in, then orange | Digital citizens fill in the gap. Record citizens: AI that learns from real people's answers in large public surveys. The chatbot kind: AI that answers from what it has read about people like them. [SC two kinds] |
| 0:51 | Everything blends into blue; the marker moves from 5.6 to 3.5 | Blended with their real answers: 3.5 points off. Close to good enough to act on. [SC small groups] |
| 0:59 | Into the real scorecard: the "Small groups gain the most" table | Tested, not claimed. Every number was checked against what real people actually said. Indian Singaporeans: 5.6 → 3.5 points off. [SC small groups] |
| 1:07 | The page flips to the short answer's bars; the two 2.7s are outlined | About as accurate as a survey twice the size. 300 people blended with both kinds of AI: 2.7 points off. 600 people alone: 2.7 points off. Singapore, a brand-new question: the median over 9 groups and 20 questions. [SC short answer, case 2] |
| 1:15 | The crowd returns, faint | AI cannot replace asking real people. With no survey at all, the chatbot alone was 5.2 points off in Singapore: the rough level only. ✓ Tested against what real people said, in Singapore and the United States. ✓ Checked whether the chatbot simply remembered published answers: no sign in three checks. [SC chatbot; memory fold] |
| 1:23 | 600 dots split into two blocks of 300; one turns blue | Next: a pilot on a real topic. Survey 600 people once. Blend 300 with both kinds of AI, and check them against the other 300. If it holds, later surveys on that topic can use 300. [SC what to do, step 5] |
| 1:28 | | **Fund a pilot.** |
| 1:33 | The poster again (the last frame is the first frame) | |

**Short cut (0:35):** the same scenes on a faster clock (up to about 3 times, easing in and out), from the poster
to "3.5 points off", then a dissolve to "Fund a pilot." and the poster. It leaves out the scorecard pages and the
limits, so use it as an opener with a link to the full film or the scorecard.

---

## Film 2: "Five lessons from building with AI" (5:33)

A teaching film for people starting to work with AI. Five chapters of about 53 seconds; each stands on its own.
Each shows King's real message as typed (typos kept), what Claude did next, the result on the real page, and the
lesson. A strip of 171 dots along the bottom marks where each message sits in the record.

**Opening (0:00 to 0:40)**
- Poster: Five lessons from building with AI. How King and Claude built it together, from the record of every message.
- 171 messages from King, over about 33 hours of work. 31 tasks, all set by King. 75 published versions of the
  scorecard. Each dot is one message, in order. [CB part 3]
- Three ways of working together: 58 Claude as a tool; 101 Claude as a teammate; 12 working independently, with
  one line each from the casebook's definitions. [CB]
- King set every task and did the judging. Claude did the building, testing and writing. [CB who did what]
- The five lesson titles.

**1. Is this backed up? (0:40)**
- King, message 53: "and is this backed up? as people over 60 often do."
- Claude: Checked the data: people over 60 were the most distinctive group on 0 of 20 questions. The example was
  replaced with Malay Singaporeans and young adults. [IX 53]
- King, message 79: "Is this backed up by evidence? - People don't fully agree with themselves. Asked the same
  question twice, most people give the same answer only about 70–80% …"
- Claude: Checked it against a Stanford study (81% of answers repeated) and our own data (69%), and corrected the
  wording. King then asked for the figures on both pages. [IX 79, 80]
- Page: "Why we score groups, not individual people". People repeat only 69 to 81% of their own answers weeks
  later. Across a group, the changes mostly cancel out. [SC]
- Lesson: A confident sentence is not evidence. Ask where each claim comes from. King challenged a claim or asked
  for its source 19 times. [CB]

**2. Why did you blend it? (1:33)**
- King, message 71: "why did you blend it? it messes up the whole analysis when you are inconsistent in your methods"
- Claude: Agreed: the page mixed three different setups. Ran one like-for-like test, and a claim about standout
  groups did not hold. [IX 71]
- King, message 72: "ok do a proper QA on accuracy, accessibility (including language), and aesthetics, and once ok,
  please rebuild"
- Claude: Ran one test for every number, in both countries, with ten draws each; had a helper agent audit it;
  rebuilt the page from it. [IX 72]
- Casebook page: every correction is logged. Small surveys, scored honestly: Claude's own error; people were checked
  against themselves, so 300 looked like 1,500. One method for everything: King noticed the page mixed setups.
  [CB tests 8 and 12; IX 13]
- Lesson: Numbers from different setups can't be compared. Insist on one method for every number, and log every
  correction, including the AI's own.

**3. Explain simply (2:27)**
- King, messages 4, 10, 14 and 19, one after another, ending "… please stop using jargon". Six times on the first
  day, King asked for a simpler explanation. [CB task 4]
- Claude: Replaced the jargon with plain words, agreed once and used everywhere: "spread" became "fill in the
  groups"; "headline number" became "the overall number". [IX 19]
- King, message 166: "Maybe make it look like an equation or something? …" Claude: Mocked up King's idea on the
  real page, in two versions. King chose one. [IX 166, 167]
- Page: King's equations. Two ways of using a person's real answers, shown as two equations that differ only in
  their coloured middle box. [SC]
- Lesson: If the person in charge can't follow it, nobody else will. Agree plain words once and keep them. When an
  explanation works, put it on the page.

**4. Stop patching (3:20)**
- King, message 101: "yes stop patching. let me give you some final comments, and then pleasse go through and make
  everything tigheer and more integrated"
- Claude: Changed nothing until all the comments were in. Then one pass over the whole page, listing every change
  before publishing. [IX 101]
- King, message 127: "Option B is good. It's easier for a team to say look at point 4 the green band etc."
  Claude: Built it: numbered sections, each on its own colour band. [IX 127]
- Page: numbered colour bands, chosen by King. [SC]
- King, message 128: "Ok can you do a thorough QA now …" Claude: Three helper agents: one recomputed every number,
  one read the page cold as an executive, one checked the companion documents. 23 findings fixed. [IX 128]
- Lesson: Many small fixes pile up into a page that contradicts itself. Collect the comments, make one integrated
  pass, then check everything again.

**5. Test it, don't argue (4:13)**
- King, message 148: "… And how do we test the ai for whether it has seen answers before ?" Claude: Proposed four
  checks for memory, cheapest first, each with its cost. [IX 148]
- King, message 151: "Ok so tests 1 and 3, then 2. …" Claude: Wrote down the warning signs before running anything,
  then ran three checks for about $5: no sign the chatbot remembered the published answers. [IX 151]
- Page: three checks, no sign of memory. Only questions asked after the chatbot was built can rule it out, so that
  is on the list to test next. [SC]
- King, messages 168 and 169: "compare this with with our digital citizens scorecard. what do you see?" / "yes do
  that". Claude: Ran the other study's method on our own data instead of debating it: blending saved about half the
  participants; theirs, about 1 in 10. [CB tests]
- Lesson: When a question can be tested cheaply, test it. Decide what counts as a warning before you look, and cap
  the spend before you start.

**Close (5:07)**
- Casebook page: Everything is written down. The scorecard, the casebook, an eight-step playbook and the code, so
  anyone can do it again. [CB part 4]
- The five lessons again; then the poster (the last frame is the first frame).

---

## Privacy
- Film 2 shows King's first name and King's messages as typed. The casebook they come from is private, so check
  before sharing Film 2 outside your circle. No survey respondent can be identified: both films show group
  results only.
- Nothing is shown from the API key, the environment settings or King's email.
