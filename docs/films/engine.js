// Shared drawing engine for the Digital Citizens films. Everything is a pure function of film time t (seconds),
// so any frame can be drawn on its own: window.renderAt(t).
const W = 1920, H = 1080;
const C = {
  bg: '#121211', bg2: '#1a1a19', ink: '#f0efec', ink2: '#c3c2b7', muted: '#898781', grid: '#2c2c2a',
  survey: '#3987e5', both: '#3987e5', rc: '#1baf7a', cb: '#eb6834', good: '#3fbf5f', dot: '#e9e6df',
};
const BPM = 90, BAR = 4 * 60 / BPM; // one bar = 2.667 s; scenes start on bars so the music can follow them
const bar = n => n * BAR;

// ---------- maths ----------
const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const lerp = (a, b, k) => a + (b - a) * k;
const smooth = k => { k = clamp(k); return k * k * (3 - 2 * k); };
const ease = k => { k = clamp(k); return k < 0.5 ? 4 * k * k * k : 1 - Math.pow(-2 * k + 2, 3) / 2; }; // in-out cubic
const easeOut = k => 1 - Math.pow(1 - clamp(k), 3);
const prog = (t, a, b) => clamp((t - a) / (b - a));
function rng(seed) { let s = seed >>> 0; return () => { s = (s * 1664525 + 1013904223) >>> 0; return s / 4294967296; }; }
function shuffle(arr, seed) { const r = rng(seed), a = arr.slice(); for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(r() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; }
// fade in over [a, a+fi], hold, fade out over [b-fo, b]
const window01 = (t, a, b, fi = 0.6, fo = 0.6) => Math.min(smooth((t - a) / fi), smooth((b - t) / fo));
function hexA(hex, a) { const n = parseInt(hex.slice(1), 16); return `rgba(${n >> 16},${(n >> 8) & 255},${n & 255},${a})`; }
function mix(h1, h2, k) {
  const a = parseInt(h1.slice(1), 16), b = parseInt(h2.slice(1), 16);
  const c = [16, 8, 0].map(s => Math.round(lerp((a >> s) & 255, (b >> s) & 255, k)));
  return '#' + c.map(v => v.toString(16).padStart(2, '0')).join('');
}

// ---------- layouts ----------
// sunflower disc of n points around (cx, cy), spacing sp
function disc(n, cx, cy, sp) {
  const out = [], g = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < n; i++) { const r = sp * Math.sqrt(i + 0.5), a = i * g; out.push([cx + r * Math.cos(a), cy + r * Math.sin(a)]); }
  return out;
}
function crowd(n, x0, y0, x1, y1, seed) { // jittered grid
  const r = rng(seed), cols = Math.round(Math.sqrt(n * (x1 - x0) / (y1 - y0))), rows = Math.ceil(n / cols);
  const dx = (x1 - x0) / cols, dy = (y1 - y0) / rows, out = [];
  for (let i = 0; i < n; i++) { const c = i % cols, rr = Math.floor(i / cols); out.push([x0 + (c + 0.5 + (r() - 0.5) * 0.7) * dx, y0 + (rr + 0.5 + (r() - 0.5) * 0.7) * dy]); }
  return out;
}

// ---------- canvas and text layers ----------
let cv, cx, layer;
function setup() {
  document.body.style.cssText = `margin:0;background:${C.bg};overflow:hidden;width:${W}px;height:${H}px`;
  const stage = document.createElement('div'); stage.id = 'stage';
  stage.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;overflow:hidden;background:${C.bg};font-family:Inter,sans-serif;color:${C.ink}`;
  document.body.appendChild(stage);
  cv = document.createElement('canvas'); cv.width = W; cv.height = H; cv.style.cssText = 'position:absolute;left:0;top:0';
  stage.appendChild(cv); cx = cv.getContext('2d');
  layer = document.createElement('div'); layer.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px`;
  stage.appendChild(layer);
  const vig = document.createElement('div');
  vig.style.cssText = `position:absolute;inset:0;pointer-events:none;background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.42) 100%)`;
  stage.appendChild(vig);
  return stage;
}
// Text blocks are made once and shown or hidden per frame.
const texts = {};
function text(id, html, css) {
  if (!texts[id]) { const d = document.createElement('div'); d.innerHTML = html; d.style.cssText = 'position:absolute;will-change:opacity,transform;' + css; layer.appendChild(d); texts[id] = d; }
  return texts[id];
}
function show(id, a, dy = 0, extra = '') {
  const d = texts[id]; if (!d) return;
  d.style.opacity = a; d.style.display = a <= 0.001 ? 'none' : 'block';
  d.style.transform = `translateY(${dy}px)` + extra;
}
// caption: fades in rising, fades out
function cap(id, t, a, b, html, css, fi = 0.7, fo = 0.6) {
  text(id, html, css);
  const k = window01(t, a, b, fi, fo);
  show(id, k, (1 - easeOut((t - a) / fi)) * 18);
}
// a stack of caption lines that share one box; each line fades in at its own time, all leave together
function capStack(id, t, a, b, lines, css, fo = 0.6) {
  if (!texts[id]) {
    const d = document.createElement('div'); d.style.cssText = 'position:absolute;' + css; layer.appendChild(d); texts[id] = d;
    d._lines = lines.map(([, html, lcss]) => { const l = document.createElement('div'); l.innerHTML = html; l.style.cssText = 'will-change:opacity,transform;' + lcss; d.appendChild(l); return l; });
  }
  const d = texts[id], kOut = smooth((b - t) / fo);
  const on = t > a && t < b;
  d.style.display = on ? 'block' : 'none';
  lines.forEach(([s, ], i) => { const k = smooth((t - a - s) / 0.7); d._lines[i].style.opacity = Math.min(k, kOut); d._lines[i].style.transform = `translateY(${(1 - easeOut((t - a - s) / 0.7)) * 18}px)`; });
}
const H1 = `font-family:'Inter Display',Inter,sans-serif;font-weight:600;font-size:64px;line-height:1.08;letter-spacing:-0.01em;color:${C.ink}`;
const H2 = `font-family:Inter,sans-serif;font-weight:400;font-size:36px;line-height:1.3;color:${C.ink2}`;
const SMALL = `font-family:Inter,sans-serif;font-weight:500;font-size:24px;line-height:1.3;color:${C.muted}`;

function clear() { cx.setTransform(1, 0, 0, 1, 0, 0); cx.fillStyle = C.bg; cx.fillRect(0, 0, W, H); }
function dot(x, y, r, col, a = 1, glow = 0) {
  if (a <= 0.002 || r <= 0.05) return;
  if (glow > 0) {
    const g = cx.createRadialGradient(x, y, 0, x, y, r * (3 + 3 * glow));
    g.addColorStop(0, hexA(col, 0.35 * a * glow)); g.addColorStop(1, hexA(col, 0));
    cx.fillStyle = g; cx.beginPath(); cx.arc(x, y, r * (3 + 3 * glow), 0, 7); cx.fill();
  }
  cx.fillStyle = hexA(col, a); cx.beginPath(); cx.arc(x, y, r, 0, 7); cx.fill();
}

// ---------- the points-off scale ----------
// x position for a value of points off on a linear 0..16 axis
function scale(t, opt) {
  const { x0, x1, y, a, v, vcol, vlabel, vlabelA = 1, ticksA = 1, prev } = opt;
  if (a <= 0.002) return;
  const X = p => p <= 8 ? x0 + (x1 - x0) * 0.8 * p / 8 : x0 + (x1 - x0) * (0.86 + 0.14 * (p - 8) / 8);
  cx.save(); cx.globalAlpha = a;
  cx.strokeStyle = C.grid; cx.lineWidth = 2; cx.beginPath(); cx.moveTo(x0, y); cx.lineTo(X(8.2), y); cx.moveTo(X(8.6), y); cx.lineTo(x1, y); cx.stroke();
  cx.strokeStyle = C.muted; cx.beginPath(); cx.moveTo(X(8.25) - 6, y + 12); cx.lineTo(X(8.25) + 6, y - 12); cx.moveTo(X(8.55) - 6, y + 12); cx.lineTo(X(8.55) + 6, y - 12); cx.stroke();
  // shaded bands
  const band = (p0, p1, col, al) => { cx.fillStyle = hexA(col, al); cx.fillRect(X(p0), y - 10, X(p1) - X(p0), 20); };
  band(0, 1.5, C.muted, 0.18); band(1.5, 3, C.good, 0.38); band(3, 5, '#d9a43a', 0.28); band(5, 8.2, C.muted, 0.10); band(8.6, 16, C.muted, 0.10);
  const ticks = [[1.5, 'Best possible', '1.5'], [3, 'Good enough to act on', '3'], [5, 'Rough level only', '5'], [15, 'Guessing blind', '15']];
  cx.textAlign = 'center';
  ticks.forEach(([p, lab, num], i) => {
    const k = clamp(ticksA * 4 - i);
    if (k <= 0) return;
    cx.globalAlpha = a * k;
    cx.fillStyle = C.ink2; cx.font = '600 26px Inter'; cx.fillText(num, X(p), y + 52);
    cx.fillStyle = C.muted; cx.font = '400 22px Inter';
    const lines = lab.split(' ').reduce((acc, w) => { const l = acc[acc.length - 1]; if ((l + ' ' + w).length > 16 && l) acc.push(w); else acc[acc.length - 1] = (l ? l + ' ' : '') + w; return acc; }, ['']);
    lines.forEach((l, j) => cx.fillText(l, X(p), y + 84 + j * 26));
    cx.strokeStyle = C.ink2; cx.lineWidth = 2; cx.beginPath(); cx.moveTo(X(p), y - 14); cx.lineTo(X(p), y + 14); cx.stroke();
  });
  cx.globalAlpha = a;
  cx.fillStyle = C.muted; cx.font = '500 22px Inter'; cx.textAlign = 'left';
  cx.fillText('POINTS OFF  ·  lower is closer to what people really said', x0, y + 168);
  if (prev) { // ghost of the earlier value
    cx.globalAlpha = a * prev.a; dot(X(prev.v), y, 11, prev.col, 0.5);
    cx.fillStyle = C.muted; cx.font = '600 26px Inter'; cx.textAlign = 'center'; cx.fillText(prev.label, X(prev.v), y - 26);
  }
  if (v != null) {
    cx.globalAlpha = a; dot(X(v), y, 14, vcol, 1, 1);
    cx.globalAlpha = a * vlabelA; cx.fillStyle = vcol; cx.font = '700 34px Inter'; cx.textAlign = 'center';
    cx.fillText(vlabel, X(v), y - 30);
  }
  cx.restore();
}

// ---------- browser window holding a real page capture ----------
// img: a loaded capture; scrollY in capture pixels; placement via a 2D/3D camera
const imgs = {};
function loadImages(list) {
  return Promise.all(list.map(([id, src]) => new Promise((res, rej) => { const im = new Image(); im.onload = () => { imgs[id] = im; res(); }; im.onerror = rej; im.src = src; })));
}
const browsers = {};
function browser(id, w, h, title) {
  if (browsers[id]) return browsers[id];
  const wrap = document.createElement('div');
  wrap.style.cssText = `position:absolute;left:0;top:0;width:${w}px;height:${h + 44}px;transform-origin:0 0;border-radius:14px;overflow:hidden;background:#fcfcfb;box-shadow:0 30px 80px rgba(0,0,0,0.55),0 0 0 1px rgba(255,255,255,0.06)`;
  wrap.innerHTML = `<div style="height:44px;background:#e9e8e3;display:flex;align-items:center;gap:9px;padding:0 18px;font:500 17px Inter;color:#52514e">
    <span style="width:13px;height:13px;border-radius:50%;background:#d3d1ca"></span><span style="width:13px;height:13px;border-radius:50%;background:#d3d1ca"></span><span style="width:13px;height:13px;border-radius:50%;background:#d3d1ca"></span>
    <span style="margin-left:18px;background:#fcfcfb;border-radius:8px;padding:5px 16px">${title}</span></div>
    <div class="vp" style="position:relative;width:${w}px;height:${h}px;overflow:hidden"></div>`;
  layer.appendChild(wrap);
  browsers[id] = { wrap, vp: wrap.querySelector('.vp'), w, h, tabs: {} };
  return browsers[id];
}
// show capture `img` in browser `b` scrolled to y (capture px are scaled to the viewport width)
function browserShow(b, layers) {
  // layers: [{img, y, a}] cross-faded
  for (const k in b.tabs) b.tabs[k].style.display = 'none';
  layers.forEach(({ img, y, a }) => {
    let el = b.tabs[img];
    if (!el) { el = document.createElement('img'); el.src = imgs[img].src; el.style.cssText = `position:absolute;left:0;top:0;width:${b.w}px`; b.vp.appendChild(el); b.tabs[img] = el; }
    const s = b.w / imgs[img].naturalWidth;
    el.style.display = a > 0.001 ? 'block' : 'none'; el.style.opacity = a;
    el.style.transform = `translateY(${-y * s}px)`;
  });
}
function place(b, x, y, s, a = 1, rx = 0, ry = 0) {
  b.wrap.style.display = a <= 0.001 ? 'none' : 'block';
  b.wrap.style.opacity = a;
  b.wrap.style.transform = `translate(${x}px,${y}px) perspective(2400px) rotateX(${rx}deg) rotateY(${ry}deg) scale(${s})`;
}
// a highlight box drawn on top of the page inside a browser window (viewport pixels)
function browserMark(b, id, x, y, w, h, a, col) {
  b.marks = b.marks || {};
  let m = b.marks[id];
  if (!m) { m = document.createElement('div'); m.style.cssText = `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;border:4px solid ${col};border-radius:12px;box-shadow:0 0 0 9999px rgba(0,0,0,0.0),0 0 30px ${col}`; b.vp.appendChild(m); b.marks[id] = m; }
  m.style.display = a <= 0.001 ? 'none' : 'block'; m.style.opacity = a;
}
