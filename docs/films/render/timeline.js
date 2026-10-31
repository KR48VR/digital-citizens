// node render/timeline.js page.html out.json : export the film's timeline (for the music and QA)
const { chromium } = require('playwright'); const path = require('path'); const fs = require('fs');
(async () => { const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.resolve(process.argv[2])); await p.evaluate(() => window.ready);
  fs.writeFileSync(process.argv[3], JSON.stringify(await p.evaluate(() => ({ duration: window.DURATION, timeline: window.TIMELINE, accents: window.ACCENTS })), null, 1)); await b.close(); })();
