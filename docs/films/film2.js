// Film 2: "Five lessons from building with AI". Same engine and bar grid as Film 1 (90 bpm).
// Colours follow the casebook: blue = tool, green = teammate, orange = independent.
const BEAT = BAR / 4;
const TYPE_COL = { tool: C.survey, teammate: C.rc, independent: C.cb };
const TYPE_NAME = { tool: 'tool', teammate: 'teammate', independent: 'independent' };
const NM = IX.length; // 171 messages
const TOP = 'left:140px;top:96px;width:1640px';
const q = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');

// ---------- the story, in bars ----------
const CHAPTERS = [
  { title: 'Is this backed up?', beats: [
    ['card', 2],
    ['ex', 4, { n: [53], claude: 'Checked the data: people over 60 were the most distinctive group on 0 of 20 questions. The example was replaced with Malay Singaporeans and young adults.' }],
    ['ex', 4.5, { n: [79], cut: 158, claude: 'Checked it against a Stanford study (81% of answers repeated) and our own data (69%), and corrected the wording. King then asked for the figures on both pages.' }],
    ['page', 5, { img: 'sc_groups', y0: 0, y1: 120, eyebrow: 'On the scorecard now', head: 'Why we score groups, not individual people',
      body: 'People repeat only 69 to 81% of their own answers weeks later. Across a group, the changes mostly cancel out.' }],
    ['lesson', 4.5, { head: 'A confident sentence is not evidence.', body: 'Ask where each claim comes from. King challenged a claim or asked for its source 19 times.' }]] },
  { title: 'Why did you blend it?', beats: [
    ['card', 2],
    ['ex', 4.5, { n: [71], claude: 'Agreed: the page mixed three different setups. Ran one like-for-like test, and a claim about standout groups did not hold.' }],
    ['ex', 4, { n: [72], claude: 'Ran one test for every number, in both countries, with ten draws each; had a helper agent audit it; rebuilt the page from it.' }],
    ['page', 5, { img: 'cb_tests', y0: 40, y1: 760, title: 'Digital Citizens Casebook', eyebrow: 'In the casebook', head: 'Every correction is logged',
      body: '<b style="color:#f0efec">Small surveys, scored honestly:</b> Claude\'s own error. People were checked against themselves, so 300 looked like 1,500.<br><br><b style="color:#f0efec">One method for everything:</b> King noticed the page mixed setups.' }],
    ['lesson', 4.5, { head: 'Numbers from different setups can\'t be compared.', body: 'Insist on one method for every number, and log every correction, including the AI\'s own.' }]] },
  { title: 'Explain simply', beats: [
    ['card', 2],
    ['montage', 4, { n: [4, 10, 14, 19], cut: 64, text: { 19: 'what do you mean "citizens spread it"? … please stop using jargon' }, note: 'Six times on the first day, King asked for a simpler explanation.' }],
    ['claude', 3, { claude: 'Replaced the jargon with plain words, agreed once and used everywhere: "spread" became "fill in the groups"; "headline number" became "the overall number".' }],
    ['ex', 3, { n: [166], cut: 52, claude: 'Mocked up King\'s idea on the real page, in two versions. King chose one.' }],
    ['page', 3.5, { img: 'sc_reading', y0: 560, y1: 640, eyebrow: 'On the scorecard now', head: 'King\'s equations',
      body: 'Two ways of using a person\'s real answers, shown as two equations that differ only in their coloured middle box.' }],
    ['lesson', 4.5, { head: 'If the person in charge can\'t follow it, nobody else will.', body: 'Agree plain words once and keep them. When an explanation works, put it on the page.' }]] },
  { title: 'Stop patching', beats: [
    ['card', 2],
    ['ex', 4, { n: [101], claude: 'Changed nothing until all the comments were in. Then one pass over the whole page, listing every change before publishing.' }],
    ['ex', 3, { n: [127], claude: 'Built it: numbered sections, each on its own colour band.' }],
    ['page', 3.5, { img: 'sc_bands', y0: 120, y1: 900, eyebrow: 'On the scorecard now', head: 'Numbered colour bands',
      body: 'Chosen by King, so a team can point to a section by its number and colour.' }],
    ['ex', 3.5, { n: [128], cut: 130, claude: 'Three helper agents: one recomputed every number, one read the page cold as an executive, one checked the companion documents. 23 findings fixed.' }],
    ['lesson', 4, { head: 'Many small fixes pile up into a page that contradicts itself.', body: 'Collect the comments, make one integrated pass, then check everything again.' }]] },
  { title: 'Test it, don\'t argue', beats: [
    ['card', 2],
    ['ex', 4, { n: [148], from: 'And how do we test', claude: 'Proposed four checks for memory, cheapest first, each with its cost.' }],
    ['ex', 3.5, { n: [151], claude: 'Wrote down the warning signs before running anything, then ran three checks for about $5: no sign the chatbot remembered the published answers.' }],
    ['page', 3.5, { img: 'sc_memory2', y0: 0, y1: 520, eyebrow: 'On the scorecard now', head: 'Three checks, no sign of memory',
      body: 'Only questions asked after the chatbot was built can rule it out, so that is on the list to test next.' }],
    ['ex', 3.5, { n: [168, 169], cut: 76, claude: 'Ran the other study\'s method on our own data instead of debating it: blending saved about half the participants; theirs, about 1 in 10.' }],
    ['lesson', 3.5, { head: 'When a question can be tested cheaply, test it.', body: 'Decide what counts as a warning before you look, and cap the spend before you start.' }]] },
];
const OPEN = { poster: 0, timeline: 2, kinds: 6, roles: 11, ch: 15 };
const BEATS = []; // [{ch, type, a, b, data, id}] in seconds
{
  let b0 = OPEN.ch;
  CHAPTERS.forEach((ch, ci) => {
    ch.start = b0;
    ch.beats.forEach(([type, len, data], k) => { BEATS.push({ ch: ci, type, a: bar(b0), b: bar(b0 + len), data: data || {}, id: `b${ci}_${k}` }); b0 += len; });
    ch.end = b0;
  });
  var CLOSE = b0; // 115
}
const S = { close: CLOSE, recap: CLOSE + 4.5, end: CLOSE + 8, stop: CLOSE + 10 };
const DURATION = bar(S.stop);
window.DURATION = DURATION;
window.TIMELINE = { bar: BAR, open: OPEN, close: S, beats: BEATS.map(b => ({ ch: b.ch, type: b.type, a: b.a / BAR, b: b.b / BAR })) };
window.ACCENTS = [{ name: 'poster', t: 0 }, { name: 'timeline', t: bar(OPEN.timeline) }, { name: 'kinds', t: bar(OPEN.kinds) }, { name: 'roles', t: bar(OPEN.roles) }]
  .concat(BEATS.map(b => ({ name: `ch${b.ch + 1}:${b.type}`, t: b.a })))
  .concat([{ name: 'close', t: bar(S.close) }, { name: 'recap', t: bar(S.recap) }, { name: 'end', t: bar(S.end) }]);

// ---------- the 171 messages as dots ----------
const GRID = [], KINDS = [], STRIP = [];
{
  const cols = 19, sp = 58;
  IX.forEach((r, i) => { const c = i % cols, rr = Math.floor(i / cols); GRID.push([960 - (cols - 1) * sp / 2 + c * sp, 560 - 8 * sp / 2 + rr * sp]); });
  const spec = { tool: [430, 9], teammate: [960, 11], independent: [1490, 4] }, cnt = { tool: 0, teammate: 0, independent: 0 };
  IX.forEach(r => { const [x, cl] = spec[r.type], k = cnt[r.type]++, s2 = 34; KINDS.push([x - (cl - 1) * s2 / 2 + (k % cl) * s2, 330 + Math.floor(k / cl) * s2]); });
  IX.forEach((r, i) => STRIP.push([170 + i * (1580 / (NM - 1)), 1028]));
}
const popAt = IX.map((r, i) => bar(OPEN.timeline) + BEAT * (0.5 + Math.floor(i / 11)));
const nIndex = {}; IX.forEach((r, i) => nIndex[r.n] = i);

function highlightAt(t) { // which messages glow on the strip
  const out = {};
  for (const b of BEATS) if ((b.type === 'ex' || b.type === 'montage') && t > b.a - 0.3 && t < b.b + 0.3)
    b.data.n.forEach((n, k) => { out[n] = Math.max(out[n] || 0, window01(t, b.a + (b.type === 'montage' ? k * 0.9 : 0), b.b, 0.5, 0.5)); });
  return out;
}

function drawMessages(t) {
  const kGrid0 = 1 - smooth(prog(t, bar(OPEN.timeline) - 0.9, bar(OPEN.timeline) - 0.1)); // poster fade
  const kEnd = smooth(prog(t, bar(S.end) + 0.2, bar(S.end) + 1.4));
  if (t < bar(OPEN.timeline) || t > bar(S.end)) { // poster: the whole record, faint
    const k = t < bar(OPEN.timeline) ? kGrid0 : kEnd;
    IX.forEach((r, i) => dot(GRID[i][0], GRID[i][1] + 60, 9, TYPE_COL[r.type], 0.24 * k, 0.15));
    return;
  }
  const kSort = t => clamp((t - bar(OPEN.kinds) - 0.4) / (BAR * 1.3));
  const kStrip = ease(prog(t, bar(OPEN.roles), bar(OPEN.roles) + BAR * 1.2));
  const kStripOut = smooth(prog(t, bar(S.end) - 0.8, bar(S.end) + 0.1));
  const hl = highlightAt(t);
  IX.forEach((r, i) => {
    if (t < popAt[i]) return;
    const ks = ease(clamp((kSort(t) - (i / NM) * 0.3) / 0.7));
    const kst = clamp((kStrip - (1 - i / NM) * 0.25) / 0.75);
    let x = lerp(GRID[i][0], KINDS[i][0], ks), y = lerp(GRID[i][1], KINDS[i][1], ks);
    x = lerp(x, STRIP[i][0], ease(kst)); y = lerp(y, STRIP[i][1], ease(kst));
    const pop = t < popAt[i] + 0.4 ? 1 + 0.7 * Math.sin(Math.PI * clamp((t - popAt[i]) / 0.4)) : 1;
    const h = hl[r.n] || 0;
    const rad = lerp(lerp(11, 10, ks), 4.2, ease(kst)) * pop + h * 5;
    const a = lerp(0.95, 0.42, ease(kst)) * easeOut((t - popAt[i]) / 0.3) + h * 0.55;
    dot(x, y, rad, TYPE_COL[r.type], a * (1 - kStripOut), 0.35 + h * 0.9);
  });
  // label for the highlighted message on the strip
  const top = Object.entries(hl).sort((a, b) => b[1] - a[1])[0];
  if (top && top[1] > 0.01) {
    const i = nIndex[top[0]], r = IX[i];
    cx.save(); cx.globalAlpha = top[1] * (1 - kStripOut); cx.fillStyle = C.muted; cx.font = '500 20px Inter';
    cx.textAlign = STRIP[i][0] > 1500 ? 'right' : STRIP[i][0] < 400 ? 'left' : 'center';
    cx.fillText(`message ${r.n} of ${NM}`, STRIP[i][0], 1000); cx.restore();
  }
}

// ---------- bubbles ----------
function kingBubble(id, n, t, a, b, top, opt = {}) {
  const r = IXT[n];
  let msg = r.king.replace(/\s*\[.*?\]\s*/g, ' ').replace(/\s+/g, ' ').trim();
  if (opt.from) msg = '… ' + msg.slice(msg.indexOf(opt.from)).trim();
  if (opt.text && opt.text[n]) msg = opt.text[n]; // a hand-made excerpt, shown whole
  else if (opt.cut && msg.length > opt.cut) msg = msg.slice(0, opt.cut).replace(/\s+\S*$/, '') + ' …';
  const col = TYPE_COL[r.type];
  if (!texts[id]) {
    text(id, `<div style="font:600 19px Inter;letter-spacing:0.12em;color:${C.muted};margin-bottom:12px">KING <span style="font-weight:500;letter-spacing:0.04em">· message ${n}</span></div>
      <div class="m" style="font:500 42px/1.3 Inter;color:${C.ink}"></div>`,
      `left:140px;top:${top}px;max-width:1500px;padding:26px 34px 30px;background:#1d1d1b;border-radius:18px;border-left:7px solid ${col};box-shadow:0 20px 50px rgba(0,0,0,0.35)`);
    texts[id]._m = texts[id].querySelector('.m');
  }
  const el = texts[id];
  el.style.top = top + 'px';
  if (el._h == null) { el._m.textContent = msg; el.style.display = 'block'; el._h = el.offsetHeight; el._m.textContent = ''; el._last = null; }
  const typeDur = Math.min(2.4, 0.4 + msg.length * 0.022);
  const kType = clamp((t - a - 0.25) / typeDur), nch = Math.round(msg.length * kType);
  const caret = kType < 1 || Math.floor((t - a) * 2) % 2 === 0 ? `<span style="color:${col}">▍</span>` : '<span style="opacity:0">▍</span>';
  const html = q(msg.slice(0, nch)) + (t < a + typeDur + 1.2 ? caret : '');
  if (texts[id]._last !== html) { texts[id]._m.innerHTML = html; texts[id]._last = html; }
  show(id, window01(t, a, b, 0.4, 0.5), (1 - easeOut((t - a) / 0.5)) * 16);
  return [typeDur, el._h];
}
function claudeBubble(id, html, t, a, b, top, left = 260) {
  text(id, `<div style="font:600 19px Inter;letter-spacing:0.12em;color:${C.muted};margin-bottom:12px">CLAUDE</div><div style="font:400 36px/1.38 Inter;color:${C.ink2}">${html}</div>`,
    `left:${left}px;top:${top}px;max-width:${1640 - left}px;padding:24px 34px 28px;border-radius:18px;border:2px solid #2e2e2b;background:#151514`);
  show(id, window01(t, a, b, 0.6, 0.5), (1 - easeOut((t - a) / 0.6)) * 16);
}

// ---------- beat drawing ----------
function drawBeat(bt, t) {
  const { a, b, data: d, id, ch } = bt;
  if (t < a - 0.05 || t > b + 0.05) { hideBeat(bt); return; }
  if (bt.type === 'card') {
    const k = window01(t, a + 0.1, b, 0.7, 0.45);
    text(id + 'n', `${ch + 1}`, `left:140px;top:250px;font:700 260px/1 'Inter Display',Inter;color:${C.ink};opacity:0.9`);
    text(id + 't', q(CHAPTERS[ch].title), `left:150px;top:540px;width:1600px;font:600 96px/1.05 'Inter Display',Inter;letter-spacing:-0.015em;color:${C.ink}`);
    text(id + 'e', `LESSON ${ch + 1} OF 5`, `left:154px;top:210px;font:600 22px Inter;letter-spacing:0.16em;color:${C.muted}`);
    show(id + 'n', k, (1 - easeOut((t - a) / 0.8)) * 24); show(id + 't', k, (1 - easeOut((t - a - 0.2) / 0.8)) * 24); show(id + 'e', k);
  }
  if (bt.type === 'ex') {
    let td = 0, y = d.n.length > 1 ? 110 : 170;
    d.n.forEach((n, k) => { const [dur, h] = kingBubble(`${id}k${k}`, n, t, a + 0.1 + k * 1.6, b, y, d); td = dur; y += h + 26; });
    const ca = a + 0.4 + (d.n.length - 1) * 1.6 + td + 0.5;
    claudeBubble(id + 'c', d.claude, t, ca, b, y + 30);
  }
  if (bt.type === 'montage') {
    let y = 96; d.n.forEach((n, k) => { const [, h] = kingBubble(`${id}k${k}`, n, t, a + 0.1 + k * 1.0, b, y, { cut: d.cut, text: d.text }); y += h + 22; });
    cap(id + 'note', t, a + d.n.length * 1.0 + 1.6, b, q(d.note), `left:140px;top:860px;width:1600px;${H2};color:${C.ink}`, 0.6, 0.5);
  }
  if (bt.type === 'claude') claudeBubble(id + 'c', d.claude, t, a + 0.2, b, 300, 140);
  if (bt.type === 'lesson') {
    const k = window01(t, a + 0.15, b, 0.7, 0.5);
    text(id + 'e', `LESSON ${ch + 1}`, `left:144px;top:300px;font:600 24px Inter;letter-spacing:0.16em;color:${C.rc}`);
    text(id + 'h', q(d.head), `left:140px;top:350px;width:1500px;font:600 80px/1.1 'Inter Display',Inter;letter-spacing:-0.01em;color:${C.ink}`);
    text(id + 'b', q(d.body), `left:144px;top:${d.head.length > 44 ? 610 : 520}px;width:1300px;${H2};font-size:40px`);
    show(id + 'e', k); show(id + 'h', k, (1 - easeOut((t - a) / 0.8)) * 20);
    show(id + 'b', window01(t, a + 1.2, b, 0.7, 0.5), (1 - easeOut((t - a - 1.2) / 0.8)) * 16);
  }
  if (bt.type === 'page') drawPage(id, t, a, b, d);
}
function hideBeat(bt) { for (const k in texts) if (k.startsWith(bt.id + 'k') || k.startsWith(bt.id + 'c') || k === bt.id + 'n' || k === bt.id + 't' || k === bt.id + 'e' || k === bt.id + 'h' || k === bt.id + 'b' || k === bt.id + 'note' || k.startsWith(bt.id + 'p')) show(k, 0); }

let BR = {};
function drawPage(id, t, a, b, d) {
  const title = d.title || 'Digital Citizens Scorecard';
  const br = BR[title] || (BR[title] = browser('br_' + title, 1060, 700, title));
  const kIn = ease(prog(t, a, a + 1.3)), kOut = smooth(prog(t, b - 0.6, b));
  place(br, lerp(1000, 120, kIn), lerp(300, 150, kIn), lerp(0.6, 1, kIn), kIn * (1 - kOut), lerp(8, 0, kIn), lerp(-14, 0, kIn));
  browserShow(br, [{ img: d.img, y: lerp(d.y0, d.y1, ease(prog(t, a + 1.0, b - 0.8))), a: 1 }]);
  capStack(id + 'p', t, a + 0.9, b - 0.15, [
    [0, d.eyebrow.toUpperCase(), `font:600 22px Inter;letter-spacing:0.14em;color:${C.rc}`],
    [0.3, q(d.head), H1 + ';font-size:52px;margin-top:14px'],
    [1.0, d.body, H2 + ';font-size:31px;margin-top:22px']], 'left:1260px;top:200px;width:560px', 0.4);
}

window.renderAt = function (t) {
  clear();
  for (const k in BR) place(BR[k], 0, 0, 1, 0);
  drawMessages(t);
  // ---- poster (start and end) ----
  const kP = t < bar(OPEN.timeline) ? 1 - smooth(prog(t, bar(OPEN.timeline) - 1.0, bar(OPEN.timeline) - 0.2)) : smooth(prog(t, bar(S.end) + 0.2, bar(S.end) + 1.4));
  text('p_e', 'DIGITAL CITIZENS', `left:0;width:${W}px;top:300px;text-align:center;font:600 26px Inter;letter-spacing:0.22em;color:${C.ink2};text-shadow:0 2px 20px rgba(0,0,0,0.9)`);
  text('p_title', 'Five lessons from building with AI', `left:0;width:${W}px;top:350px;text-align:center;font:600 104px/1.05 'Inter Display',Inter;letter-spacing:-0.02em;color:${C.ink};text-shadow:0 4px 40px rgba(0,0,0,0.85)`);
  text('p_sub', 'How King and Claude built it together, from the record of every message', `left:0;width:${W}px;top:600px;text-align:center;font:400 40px Inter;color:${C.ink2};text-shadow:0 2px 24px rgba(0,0,0,0.9)`);
  text('p_credit', 'Built by King and Claude', `left:0;width:${W}px;top:968px;text-align:center;font:500 24px Inter;letter-spacing:0.04em;color:${C.muted}`);
  ['p_e', 'p_title', 'p_sub', 'p_credit'].forEach(k => show(k, kP));

  // ---- opening ----
  capStack('o_tl', t, bar(OPEN.timeline) + 0.3, bar(OPEN.kinds) - 0.1, [
    [0, '171 messages from King, over about 33 hours of work.', H1],
    [2.2, '31 tasks, all set by King. 75 published versions of the scorecard. Each dot is one message, in order.', H2 + ';margin-top:14px;max-width:1500px']], TOP);
  capStack('o_kinds', t, bar(OPEN.kinds) + 0.2, bar(OPEN.roles) - 0.1, [[0, 'Three ways of working together.', H1]], TOP);
  const kl = (id, x, col, num, head, body, d0) => cap(id, t, bar(OPEN.kinds) + d0, bar(OPEN.roles) - 0.1,
    `<div style="font:700 56px 'Inter Display',Inter;color:${col}">${num}</div><div style="font:600 30px Inter;color:${C.ink};margin:4px 0 10px">${head}</div><div style="font:400 23px/1.4 Inter;color:${C.ink2}">${body}</div>`,
    `left:${x - 230}px;width:460px;top:690px;text-align:center`, 0.7, 0.5);
  kl('k_tool', 430, C.survey, 58, 'Claude as a tool', 'King asked for a defined output, such as an explanation or an edit, and Claude produced it.', 2.0);
  kl('k_team', 960, C.rc, 101, 'Claude as a teammate', 'Both shaped the result: an idea, a challenge, a pushback or a problem found changed the plan.', 2.5);
  kl('k_ind', 1490, C.cb, 12, 'Working independently', 'One worked without the other for a long stretch, such as Claude running tests for up to an hour.', 3.0);
  capStack('o_roles', t, bar(OPEN.roles) + 0.3, bar(OPEN.ch) - 0.1, [
    [0, 'King set every task and did the judging.', H1],
    [1.2, 'Claude did the building, testing and writing.', H1],
    [bar(1.6), 'Five lessons from the record of every message:', H2 + ';margin-top:40px'],
    ...CHAPTERS.map((c, i) => [bar(1.6) + 0.6 + i * 0.45, `<span style="color:${C.muted};font-weight:600;margin-right:18px">${i + 1}</span>${q(c.title)}`, H2 + ';color:#f0efec;margin-top:6px'])], TOP, 0.5);

  // ---- chapters ----
  for (const bt of BEATS) drawBeat(bt, t);

  // ---- close ----
  const cb = BR['Digital Citizens Casebook'] || (BR['Digital Citizens Casebook'] = browser('br_cb', 1060, 700, 'Digital Citizens Casebook'));
  if (t > bar(S.close) && t < bar(S.recap)) {
    const kIn = ease(prog(t, bar(S.close), bar(S.close) + 1.3)), kOut = smooth(prog(t, bar(S.recap) - 0.6, bar(S.recap)));
    place(cb, lerp(1000, 120, kIn), lerp(300, 150, kIn), lerp(0.6, 1, kIn), kIn * (1 - kOut), lerp(8, 0, kIn), lerp(-14, 0, kIn));
    browserShow(cb, [{ img: 'cb_package', y: lerp(0, 520, ease(prog(t, bar(S.close) + 1.2, bar(S.recap) - 0.8))), a: 1 }]);
  }
  capStack('c_pkg', t, bar(S.close) + 0.9, bar(S.recap) - 0.15, [
    [0, 'IN THE CASEBOOK', `font:600 22px Inter;letter-spacing:0.14em;color:${C.rc}`],
    [0.3, 'Everything is written down.', H1 + ';font-size:52px;margin-top:14px'],
    [1.0, 'The scorecard, the casebook, an eight-step playbook and the code, so anyone can do it again.', H2 + ';font-size:31px;margin-top:22px']], 'left:1260px;top:200px;width:560px', 0.4);
  capStack('c_recap', t, bar(S.recap) + 0.2, bar(S.end) - 0.05, [
    [0, 'Five lessons', `font:600 24px Inter;letter-spacing:0.16em;color:${C.rc};text-transform:uppercase`],
    ...CHAPTERS.map((c, i) => [0.3 + i * 0.35, `<span style="color:${C.muted};margin-right:22px">${i + 1}</span>${q(c.title)}`, H1 + ';font-size:58px;margin-top:10px'])],
    'left:140px;top:170px;width:1640px', 0.6);
};

window.ready = (async () => {
  setup();
  await loadImages(['sc_groups', 'cb_tests', 'sc_reading', 'sc_bands', 'sc_memory2', 'cb_package'].map(n => [n, `shots/${n}.png`]));
  for (const f of ["600 64px 'Inter Display'", "700 80px 'Inter Display'", '400 36px Inter', '500 42px Inter', '600 22px Inter']) await document.fonts.load(f);
  await document.fonts.ready;
  window.renderAt(0);
  return true;
})();
