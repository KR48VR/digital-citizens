// node render/render.js page.html out.mp4 f0 f1 [fps]  -> frames f0..f1-1 encoded as a near-lossless chunk
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path');
(async () => {
  const [,, page_, out, f0s, f1s, fpss] = process.argv;
  const fps = +(fpss || 24), f0 = +f0s, f1 = +f1s;
  const b = await chromium.launch({ args: ['--font-render-hinting=none'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('pageerror', e => { console.log('pageerror:', e.message); process.exit(1); });
  await p.goto('file://' + path.resolve(page_));
  await p.evaluate(() => window.ready);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '10', '-pix_fmt', 'yuv420p', out], { stdio: ['pipe', 'inherit', 'inherit'] });
  const t0 = Date.now();
  for (let f = f0; f < f1; f++) {
    await p.evaluate(t => window.renderAt(t), f / fps);
    const buf = await p.screenshot({ type: 'png' });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if ((f - f0) % 240 === 0) console.log(`${out}: frame ${f} (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  }
  ff.stdin.end();
  await new Promise(r => ff.on('close', r));
  console.log(`${out}: done ${f1 - f0} frames in ${((Date.now() - t0) / 1000).toFixed(0)} s`);
  await b.close();
})();
