// Capture tall strips of the real scorecard page (light mode, 1280 wide, 1.5x) for the films.
const { chromium } = require('playwright');
const [,, page_, out, ...specs] = process.argv; // spec: name:selectorOrY:height[:open]
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: +(process.env.VW||860), height: 800 }, deviceScaleFactor: 2, colorScheme: 'light' });
  await p.goto('file://' + require('path').resolve(page_));
  await p.evaluate(() => document.fonts.ready);
  for (const s of specs) {
    const [name, sel, hh, open] = s.split('|');
    if (open) await p.evaluate(ids => ids.split(',').forEach(id => { const e = document.getElementById(id); if (e) e.open = true; }), open);
    await p.waitForTimeout(150);
    const y = isNaN(+sel) ? (await p.locator(sel).first().evaluate(e => e.getBoundingClientRect().top + scrollY)) - 24 : +sel;
    await p.screenshot({ path: `${out}/${name}.png`, fullPage: true, clip: { x: 0, y, width: +(process.env.VW||860), height: +hh } });
    console.log(name, Math.round(y));
  }
  await b.close();
})();
