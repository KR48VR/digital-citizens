// Film 1: "Every group heard". Scenes start on bars (90 bpm) so the score can follow them.
// Colours follow the scorecard's chart: green = record citizens, orange = the chatbot, blue = both blended in.
const TOP = 'left:140px;top:96px;width:1640px';
const N = 300, GROUPS = { C: 231, M: 35, I: 28, O: 6 };
const S = { // scene starts, in bars
  poster: 0, survey: 2, sort: 5, shaky: 9, ai: 15, blend: 19, page: 22, bars: 25, honest: 28, pilot: 31, end: 35, stop: 37,
};
const DURATION = bar(S.stop);
const BEAT = BAR / 4;
window.DURATION = DURATION;
window.ACCENTS = Object.entries(S).map(([k, b]) => ({ name: k, bar: b, t: bar(b) }));

// who is who: a seeded shuffle so the groups are spread through the crowd
const order = shuffle([...Array(N).keys()], 7);
const grp = Array(N);
{ let i = 0; for (const [g, n] of Object.entries(GROUPS)) for (let k = 0; k < n; k++) grp[order[i++]] = g; }
const idxIn = {}; for (const g in GROUPS) idxIn[g] = []; for (let i = 0; i < N; i++) idxIn[grp[i]].push(i);
const rnd = rng(11); const jit = [...Array(N)].map(() => [rnd(), rnd(), rnd(), rnd()]);

const L_CROWD = crowd(N, 170, 320, 1750, 940, 3);
const CENTRES = { C: [600, 600, 15], M: [1110, 600, 15], I: [1420, 600, 15], O: [1665, 600, 15] };
const L_GROUPS = Array(N);
for (const g in GROUPS) { const [x, y, sp] = CENTRES[g]; const d = disc(GROUPS[g], x, y, sp); idxIn[g].forEach((i, k) => L_GROUPS[i] = d[k]); }
const FX = 1420, FY = 470; // where the 28 gather
const L_FOCUS = Array(N);
{ const d = disc(28, FX, FY, 24); idxIn.I.forEach((i, k) => L_FOCUS[i] = d[k]); }
for (let i = 0; i < N; i++) if (!L_FOCUS[i]) L_FOCUS[i] = L_GROUPS[i];

// the moment each dot pops in (on beats), during the survey scene
const popAt = Array(N); order.forEach((i, k) => popAt[i] = bar(S.survey) + BEAT * (1 + Math.floor(k / 25)));

function posterDots(k) { // the poster: a faint crowd, the 28 blue (heard, once blended)
  if (k <= 0.001) return;
  for (let i = 0; i < N; i++) if (grp[i] !== 'I') dot(L_CROWD[i][0], L_CROWD[i][1], 7, C.dot, 0.32 * k);
  for (let i = 0; i < N; i++) if (grp[i] === 'I') dot(L_CROWD[i][0], L_CROWD[i][1], 8, C.both, 0.95 * k, 0.8);
}

function dotsAt(t) {
  const out = [];
  const kSort = clamp((t - bar(S.sort)) / (BAR * 1.6));
  const kFocus = ease(prog(t, bar(S.shaky), bar(S.shaky) + BAR * 1.4));
  const kName = smooth(prog(t, bar(S.sort + 2.2), bar(S.sort + 2.2) + 0.8));
  const kBlend = smooth(prog(t, bar(S.blend) + 0.3, bar(S.blend) + 2 * BEAT));
  const shake = smooth(prog(t, bar(S.shaky) + 1.2, bar(S.shaky) + 2.5)) * (1 - smooth(prog(t, bar(S.blend), bar(S.blend) + 2 * BEAT)));
  for (let i = 0; i < N; i++) {
    const g = grp[i], j = jit[i];
    const ks = ease(clamp((kSort - j[0] * 0.35) / 0.65));
    let x = lerp(L_CROWD[i][0], L_GROUPS[i][0], ks), y = lerp(L_CROWD[i][1], L_GROUPS[i][1], ks);
    x = lerp(x, L_FOCUS[i][0], kFocus); y = lerp(y, L_FOCUS[i][1], kFocus);
    let r = 7, a = 0.9 * easeOut((t - popAt[i]) / 0.35), col = C.dot, glow = 0;
    if (t < popAt[i]) a = 0;
    if (t >= popAt[i] && t < popAt[i] + 0.5) r *= 1 + 0.6 * Math.sin(Math.PI * clamp((t - popAt[i]) / 0.5));
    if (g === 'I') {
      col = mix('#ffffff', C.both, kBlend); glow = 0.55 * kName + 0.3 * kBlend; r = lerp(r, 9, kFocus);
      x += shake * 9 * Math.sin(t * 7.1 + j[1] * 40); y += shake * 9 * Math.cos(t * 6.3 + j[2] * 40);
    } else { a *= lerp(1, 0.5, kName); a *= lerp(1, 0.14, kFocus); }
    out.push([x, y, r, col, a, glow]);
  }
  return out;
}

// record citizens (green) and the chatbot (orange) streaming in to fill in the gap
const NG = 220, NO = 110, flows = [];
{
  const r = rng(21);
  for (let k = 0; k < NG + NO; k++) {
    const green = k < NG;
    const ang = (green ? -0.5 : 0.5) + (r() - 0.5) * 2.4;
    const sx = FX + Math.cos(ang) * 1250, sy = FY + Math.sin(ang) * 820;
    const ha = r() * Math.PI * 2, hr = 150 + r() * 115;
    const ca = ang + (r() - 0.5) * 1.4;
    const ts = green ? bar(S.ai) + 0.6 + (k / NG) * BAR * 1.5 : bar(S.ai + 2) + 0.2 + ((k - NG) / NO) * BAR * 1.2;
    const ia = r() * Math.PI * 2, ir = 120 * Math.sqrt(r());
    flows.push({ green, sx, sy, cx1: FX + Math.cos(ca) * 620, cy1: FY + Math.sin(ca) * 460, ex: FX + Math.cos(ha) * hr, ey: FY + Math.sin(ha) * hr * 0.92,
      ts, ix: FX + Math.cos(ia) * ir, iy: FY + Math.sin(ia) * ir, ph: r() * 6.28 });
  }
}
function drawFlows(t, fade) {
  const kB = ease(prog(t, bar(S.blend) + 0.3, bar(S.blend) + 2 * BEAT + 0.3));
  for (const f of flows) {
    if (t < f.ts) continue;
    const k = ease((t - f.ts) / 1.9), u = 1 - k;
    let x = u * u * f.sx + 2 * u * k * f.cx1 + k * k * f.ex, y = u * u * f.sy + 2 * u * k * f.cy1 + k * k * f.ey;
    x += Math.sin(t * 0.7 + f.ph) * 5 * k; y += Math.cos(t * 0.6 + f.ph) * 5 * k;
    x = lerp(x, f.ix, kB); y = lerp(y, f.iy, kB);
    dot(x, y, lerp(3.4, 2.6, kB), f.green ? C.rc : C.cb, fade * lerp(0.85, 0.32, kB) * smooth((t - f.ts) / 0.4));
  }
  if (kB > 0) { // the blended answer: one soft blue glow
    const g = cx.createRadialGradient(FX, FY, 0, FX, FY, 260);
    g.addColorStop(0, hexA(C.both, 0.22 * kB * fade)); g.addColorStop(1, hexA(C.both, 0));
    cx.fillStyle = g; cx.beginPath(); cx.arc(FX, FY, 260, 0, 7); cx.fill();
  }
}

function markerValue(t) { // the marker wobbles, settles on 5.6, then moves to 3.5 when blended
  const t0 = bar(S.shaky) + 2.0, k = t - t0;
  if (k < 0) return 5.6 + 3.2;
  const shaky = 5.6 + 3.2 * Math.exp(-k * 1.25) * Math.cos(k * 5.2);
  return lerp(shaky, 3.5, ease(prog(t, bar(S.blend) + 0.3, bar(S.blend) + 2 * BEAT)));
}

// the pilot: 600 people, split 300 / 300
const PIL = [];
{
  const sp = 21, cols = 20, rows = 15;
  for (let k = 0; k < 600; k++) {
    const half = k < 300 ? 0 : 1, i = k % 300, c = i % cols, r = Math.floor(i / cols);
    const xJoin = 960 - (2 * cols * sp) / 2 + (half * cols + c + 0.5) * sp;
    const xSplit = (half ? 1290 : 630) - (cols * sp) / 2 + (c + 0.5) * sp;
    PIL.push({ half, xJoin, xSplit, y: 600 - (rows * sp) / 2 + (r + 0.5) * sp, pop: (half * cols + c) / (2 * cols) });
  }
}
function drawPilot(t, fade) {
  const t0 = bar(S.pilot);
  const kSplit = ease(prog(t, t0 + 2.4, t0 + 3.6)), kTint = smooth(prog(t, t0 + 3.4, t0 + 4.4));
  for (const p of PIL) {
    const tp = t0 + 0.6 + p.pop * 1.4;
    if (t < tp) continue;
    const a = fade * 0.9 * easeOut((t - tp) / 0.3);
    const x = lerp(p.xJoin, p.xSplit, kSplit);
    if (p.half === 0) dot(x, p.y, 5.5, mix(C.dot, C.both, kTint), a, 0.35 * kTint);
    else dot(x, p.y, 5.5, C.dot, a * lerp(1, 0.6, kTint));
  }
  if (kTint > 0) { // the two kinds of AI around the blended half
    const r = rng(5);
    for (let k = 0; k < 90; k++) {
      const ang = r() * 6.283, rad = 245 + r() * 40, col = k % 3 === 2 ? C.cb : C.rc;
      dot(630 + Math.cos(ang + t * 0.05) * rad * 1.05, 600 + Math.sin(ang + t * 0.05) * rad * 0.7, 2.6, col, fade * 0.55 * kTint);
    }
  }
}

window.renderAt = function (t) {
  clear();
  // ---- poster, at the start and the end (the last frame is the first frame) ----
  const kP0 = 1 - smooth(prog(t, bar(S.survey) - 1.0, bar(S.survey) - 0.2));
  const kP1 = smooth(prog(t, bar(S.end) + 0.2, bar(S.end) + 1.4));
  const kP = t < bar(S.survey) ? kP0 : kP1;
  posterDots(kP);
  text('p_title', 'Digital Citizens', `left:0;width:${W}px;top:356px;text-align:center;font:600 132px 'Inter Display',Inter;letter-spacing:-0.02em;color:${C.ink};text-shadow:0 4px 40px rgba(0,0,0,0.8)`);
  text('p_sub', 'Hear every group, even the small ones.', `left:0;width:${W}px;top:530px;text-align:center;font:400 46px Inter;color:${C.ink2};text-shadow:0 2px 24px rgba(0,0,0,0.9)`);
  text('p_credit', 'Built by King and Claude', `left:0;width:${W}px;top:968px;text-align:center;font:500 24px Inter;letter-spacing:0.04em;color:${C.muted}`);
  show('p_title', kP); show('p_sub', kP); show('p_credit', kP);

  // ---- the people, the AI, the scale ----
  if (t >= bar(S.survey) && t < bar(S.page) + 1) {
    const fade = 1 - smooth(prog(t, bar(S.page) - 0.2, bar(S.page) + 0.8));
    const ds = dotsAt(t);
    cx.save(); cx.globalAlpha = fade;
    for (const d of ds) if (!d[5]) dot(d[0], d[1], d[2], d[3], d[4], 0);
    drawFlows(t, 1);
    for (const d of ds) if (d[5]) dot(d[0], d[1], d[2], d[3], d[4], d[5]);
    cx.restore();
  }
  capStack('c_survey', t, bar(S.survey) + 0.3, bar(S.sort) - 0.1, [
    [0, 'Before a policy changes, you ask people what they think.', H1],
    [2.3, 'A survey of 300 Singaporeans. Each dot is one person.', H2 + ';margin-top:14px']], TOP);
  capStack('c_sort', t, bar(S.sort) + 0.4, bar(S.shaky) - 0.1, [
    [0, 'Most are Chinese Singaporeans.', H1],
    [bar(2.2) - 0.4, 'Only about 28 are <span style="color:#fff;text-shadow:0 0 24px rgba(255,255,255,0.55)">Indian Singaporeans</span>.', H1]], TOP);
  const lab = (id, g, html, a0) => {
    const [x, y, sp] = CENTRES[g], rr = sp * Math.sqrt(GROUPS[g]);
    cap(id, t, bar(S.sort) + a0, bar(S.shaky) - 0.1, html, `left:${x - 200}px;width:400px;top:${Math.max(y + rr + 26, 760)}px;text-align:center;${SMALL};color:${C.ink2}`);
  };
  lab('l_c', 'C', '<b style="color:#f0efec;font-size:30px">about 231</b><br>Chinese Singaporeans', 2.6);
  lab('l_m', 'M', '<b style="color:#f0efec;font-size:30px">about 35</b><br>Malay', 3.0);
  lab('l_o', 'O', '<b style="color:#f0efec;font-size:30px">a few</b><br>others', 3.3);
  lab('l_i', 'I', '<b style="color:#fff;font-size:30px">about 28</b><br>Indian', bar(2.2));

  capStack('c_shaky', t, bar(S.shaky) + 0.5, bar(S.ai) - 0.1, [
    [0, 'An answer read off 28 people is shaky.', H1],
    [1.9, 'In our test, their answer came out 5.6 points off what Indian Singaporeans really think.', H2 + ';margin-top:14px;max-width:900px'],
    [bar(2) - 0.5, 'Points off: how far an answer is from what people really said, in percentage points.', SMALL + ';font-size:26px;margin-top:28px;max-width:760px']], TOP);
  const dotg = c => `<span style="display:inline-block;width:20px;height:20px;border-radius:50%;background:${c};margin-right:14px;vertical-align:-1px;box-shadow:0 0 14px ${c}"></span>`;
  capStack('c_ai', t, bar(S.ai) + 0.2, bar(S.blend) - 0.1, [
    [0, 'Digital citizens fill in the gap.', H1],
    [0.8, `${dotg(C.rc)}<b style="color:${C.ink}">Record citizens:</b> AI that learns from real people's answers in large public surveys.`, H2 + ';margin-top:22px;max-width:960px'],
    [bar(2), `${dotg(C.cb)}<b style="color:${C.ink}">The chatbot kind:</b> AI that answers from what it has read about people like them.`, H2 + ';margin-top:18px;max-width:960px']], TOP);
  capStack('c_blend', t, bar(S.blend) + 0.4, bar(S.page) - 0.1, [
    [0, 'Blended with their real answers:', H1],
    [0.8, `<span style="color:${C.both}">3.5 points off.</span>`, H1],
    [2.0, 'Close to good enough to act on.', H2 + ';margin-top:14px']], TOP);
  const kMove = ease(prog(t, bar(S.blend) + 0.3, bar(S.blend) + 2 * BEAT));
  const kScale = window01(t, bar(S.shaky) + 1.4, bar(S.page) - 0.2, 0.9, 0.8);
  scale(t, {
    x0: 200, x1: 1720, y: 800, a: kScale, v: t < bar(S.shaky) + 2.0 ? null : markerValue(t), vcol: mix(C.ink, C.both, kMove),
    vlabel: kMove < 0.5 ? '5.6 points off' : '3.5 points off',
    vlabelA: smooth(prog(t, bar(S.shaky) + 3.6, bar(S.shaky) + 4.2)) * Math.abs(1 - 2 * kMove),
    ticksA: clamp(prog(t, bar(S.shaky + 2), bar(S.shaky + 3.5))),
    prev: kMove > 0 ? { v: 5.6, col: C.ink, a: kMove, label: 'survey alone' } : null,
  });

  // ---- the real pages ----
  const b = browser('sc', 1060, 700, 'Digital Citizens Scorecard');
  const kIn = ease(prog(t, bar(S.page), bar(S.page) + 1.6));
  const kOut = smooth(prog(t, bar(S.honest) - 0.7, bar(S.honest) - 0.05));
  if (t > bar(S.page) && t < bar(S.honest)) {
    const push = ease(prog(t, bar(S.bars) + 0.4, bar(S.honest) - 0.6)) * 0.06;
    place(b, lerp(980, 120, kIn) - push * 900, lerp(330, 150, kIn) - push * 300, lerp(0.55, 1, kIn) + push, kIn * (1 - kOut), lerp(10, 0, kIn), lerp(-16, 0, kIn));
    const kTab = smooth(prog(t, bar(S.bars) - 0.25, bar(S.bars) + 0.25)); // flip to the next page, like a tab
    browserShow(b, [
      { img: 'sc_small', y: lerp(0, 250, ease(prog(t, bar(S.page) + 1.2, bar(S.page) + 3.2))), a: 1 - kTab },
      { img: 'sc_cases', y: lerp(380, 560, ease(prog(t, bar(S.bars), bar(S.bars) + 2.2))), a: kTab }]);
    browserMark(b, 'm_both', 530, 314, 420, 122, smooth(prog(t, bar(S.bars) + 3.0, bar(S.bars) + 3.6)) * (1 - kOut), C.both);
  } else place(b, 0, 0, 1, 0);
  const PANEL = 'left:1260px;top:220px;width:560px';
  capStack('c_page', t, bar(S.page) + 1.2, bar(S.bars) - 0.3, [
    [0, 'Tested, not claimed.', H1 + ';font-size:56px'],
    [0.8, 'Every number was checked against what real people actually said.', H2 + ';font-size:32px;margin-top:16px'],
    [2.2, `Indian Singaporeans:<br><span style="color:${C.ink};font-size:52px;font-weight:600">5.6 → 3.5</span><br>points off`, H2 + ';font-size:30px;margin-top:40px']], PANEL, 0.4);
  capStack('c_bars', t, bar(S.bars) + 0.4, bar(S.honest) - 0.3, [
    [0, 'About as accurate as a survey twice the size.', H1 + ';font-size:56px'],
    [1.4, `<span style="color:${C.both};font-weight:600">300 people</span> blended with both kinds of AI: 2.7 points off.`, H2 + ';font-size:32px;margin-top:22px'],
    [2.6, '<b style="color:#f0efec">600 people</b> alone: 2.7 points off.', H2 + ';font-size:32px;margin-top:14px'],
    [3.6, 'Singapore, a brand-new question: the median over 9 groups and 20 questions.', SMALL + ';margin-top:30px']], PANEL, 0.4);

  // ---- honest: the crowd returns, faint ----
  { const k = window01(t, bar(S.honest) - 0.2, bar(S.pilot) + 0.2, 1.2, 0.8); if (k > 0) for (let i = 0; i < N; i++) dot(L_CROWD[i][0], L_CROWD[i][1] + 40, 6, grp[i] === 'I' ? C.both : C.dot, k * (grp[i] === 'I' ? 0.35 : 0.1)); }
  const chk = `<span style="color:${C.good};font-weight:700;margin-right:14px">✓</span>`;
  capStack('c_honest', t, bar(S.honest) + 0.3, bar(S.pilot) - 0.1, [
    [0, 'AI cannot replace asking real people.', H1],
    [1.3, 'With no survey at all, the chatbot alone was 5.2 points off in Singapore: the rough level only.', H2 + ';margin-top:16px;max-width:1100px'],
    [bar(1.3), `${chk}Tested against what real people said, in Singapore and the United States.`, H2 + ';margin-top:56px;color:#f0efec'],
    [bar(2), `${chk}Checked whether the chatbot simply remembered published answers: no sign in three checks.`, H2 + ';margin-top:18px;color:#f0efec;max-width:1300px']],
    'left:140px;top:300px;width:1640px');

  // ---- the ask ----
  if (t > bar(S.pilot) && t < bar(S.end) + 0.5) drawPilot(t, 1 - smooth(prog(t, bar(S.end) - 0.5, bar(S.end) + 0.2)));
  capStack('c_pilot', t, bar(S.pilot) + 0.2, bar(S.end) - 0.1, [
    [0, 'Next: a pilot on a real topic.', H1],
    [1.0, 'Survey 600 people once. Blend 300 with both kinds of AI, and check them against the other 300.', H2 + ';margin-top:14px;max-width:1300px'],
    [bar(1.6), 'If it holds, later surveys on that topic can use 300.', H2 + ';margin-top:8px']], TOP, 0.5);
  const pl = (id, x, html, a0) => cap(id, t, bar(S.pilot) + a0, bar(S.end) - 0.1, html, `left:${x - 260}px;width:520px;top:812px;text-align:center;${SMALL};color:${C.ink2}`, 0.6, 0.5);
  pl('pl_a', 630, `<b style="color:${C.both};font-size:28px">300</b><br>blended with both kinds of AI`, 4.0);
  pl('pl_b', 1290, '<b style="color:#f0efec;font-size:28px">300</b><br>kept aside to check against', 4.3);
  cap('pl_fund', t, bar(S.pilot + 2), bar(S.end) - 0.05, 'Fund a pilot.', `left:0;width:${W}px;top:910px;text-align:center;font:700 80px 'Inter Display',Inter;color:#fff;letter-spacing:-0.01em;text-shadow:0 0 40px rgba(57,135,229,0.6)`, 0.7, 0.45);
};

window.ready = (async () => {
  setup();
  await loadImages([['sc_small', 'shots/sc_small.png'], ['sc_cases', 'shots/sc_cases.png']]);
  await document.fonts.load("600 64px 'Inter Display'"); await document.fonts.load("700 80px 'Inter Display'");
  await document.fonts.load('400 36px Inter'); await document.fonts.load('700 34px Inter');
  await document.fonts.ready;
  window.renderAt(0);
  return true;
})();
