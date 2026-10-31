// The short cut of Film 1 (about 35 seconds): the same scenes on a second clock. Each segment maps a stretch of film time
// (in bars, so the cut's own score can follow it) onto a stretch of Film 1's story time. The speed is smoothed
// (Gaussian, 0.22 s) so it always eases in and out. Two parts, joined by a dissolve made in ffmpeg:
// ?part=A runs to the end of the blend; ?part=B is the ask and the poster.
const PART = new URLSearchParams(location.search).get('part') || 'A';
const XF = 8 / 24; // dissolve length, seconds
const SEGS = PART === 'A'
  ? [[0, 1, 2.67, 5.33], [1, 3, 5.33, 13.33], [3, 5, 13.33, 24], [5, 7, 24, 40], [7, 10, 40, 50.67], [10, 11, 50.67, 56]]
  : [[11, 12, 88, 93.33], [12, 13, 93.33, 98.6667]];
const CUT_BARS = 13;
(function () {
  const dt = 1 / 240, c0 = bar(SEGS[0][0]) - (PART === 'B' ? XF : 0), c1 = bar(SEGS[SEGS.length - 1][1]) + (PART === 'A' ? XF : 0);
  const n = Math.ceil((c1 - c0) / dt) + 1, v = new Float64Array(n);
  for (let i = 0; i < n; i++) {
    const t = c0 + i * dt;
    let s = SEGS.find(([a, b]) => t >= bar(a) && t < bar(b)) || (t < bar(SEGS[0][0]) ? SEGS[0] : SEGS[SEGS.length - 1]);
    v[i] = (s[3] - s[2]) / (bar(s[1]) - bar(s[0]));
  }
  const sig = 0.22 / dt, R = Math.ceil(3 * sig), ker = [];
  let ks = 0; for (let k = -R; k <= R; k++) { const w = Math.exp(-0.5 * (k / sig) ** 2); ker.push(w); ks += w; }
  const vs = new Float64Array(n);
  for (let i = 0; i < n; i++) { let acc = 0; for (let k = -R; k <= R; k++) acc += ker[k + R] * v[Math.min(n - 1, Math.max(0, i + k))]; vs[i] = acc / ks; }
  // integrate, anchored so the part's first segment starts on its story time
  const st = new Float64Array(n); const anchor = Math.round((bar(SEGS[0][0]) - c0) / dt);
  for (let i = 1; i < n; i++) st[i] = st[i - 1] + vs[i - 1] * dt;
  const off = SEGS[0][2] - st[anchor];
  const story = t => { const x = (t - c0) / dt, i = Math.max(0, Math.min(n - 2, Math.floor(x))), f = x - i; return off + st[i] * (1 - f) + st[i + 1] * f; };
  const film1 = window.renderAt;
  window.CUT = { c0, c1, story };
  window.renderAt = t => film1(story(c0 + t)); // frame 0 of each part is at cut time c0
  window.DURATION = c1 - c0;
})();
