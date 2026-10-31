// node render/stills.js film1.html outdir t1 t2 ...  -> PNG per time
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [,, page_, out, ...ts] = process.argv;
  const b = await chromium.launch({ args: ['--font-render-hinting=none'] });
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  p.on('console', m => { if (m.type() === 'error') console.log('console:', m.text()); });
  p.on('pageerror', e => console.log('pageerror:', e.message));
  await p.goto('file://' + path.resolve(page_));
  await p.evaluate(() => window.ready);
  for (const t of ts) { await p.evaluate(t => window.renderAt(t), +t); await p.screenshot({ path: `${out}/t${(+t).toFixed(2).padStart(7, '0')}.png` }); }
  console.log('duration', await p.evaluate(() => window.DURATION));
  await b.close();
})();
