// node cap/cap2.js page.html outdir specs.json : [{name, sel, h, open:[ids], dy}] ; opens the details around sel too
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const [,, page_, out, specf] = process.argv;
  const specs = JSON.parse(fs.readFileSync(specf));
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 860, height: 800 }, deviceScaleFactor: 2, colorScheme: 'light' });
  await p.goto('file://' + path.resolve(page_));
  await p.evaluate(() => document.fonts.ready);
  for (const s of specs) {
    await p.evaluate(ids => { document.querySelectorAll('details').forEach(d => d.open = false); (ids || []).forEach(id => { const e = document.getElementById(id); if (e) e.open = true; }); }, s.open);
    const loc = p.locator(s.sel).first();
    await loc.evaluate(e => { let d = e.closest('details'); while (d) { d.open = true; d = d.parentElement.closest('details'); } if (e.tagName === 'DETAILS') e.open = true; });
    await p.waitForTimeout(200);
    const y = (await loc.evaluate(e => e.getBoundingClientRect().top + scrollY)) - (s.dy ?? 24);
    await p.screenshot({ path: `${out}/${s.name}.png`, fullPage: true, clip: { x: 0, y, width: 860, height: s.h } });
    console.log(s.name, Math.round(y));
  }
  await b.close();
})();
