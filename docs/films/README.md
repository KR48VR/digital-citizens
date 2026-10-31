# Films

Two short films about Digital Citizens, made in code: every frame is drawn by a web page (`renderAt(t)`),
recorded with Playwright and encoded with ffmpeg; the music is synthesised in numpy (no rights issues).

| Film | Length | For | Source |
|---|---|---|---|
| **Every group heard** | 1:39 | Funders and government: why this matters, the proof, and the ask (fund a pilot) | `film1.html`, `film1.js` |
| **Every group heard, short cut** | 0:35 | Social media and openers: the same scenes on a faster clock | `film1cut.html`, `cut.js` |
| **Five lessons from building with AI** | 5:33 | A teaching film: five chapters of about a minute, each one real moment from King and Claude's record | `film2.html`, `film2.js`, `ix.js` |

`scripts.md` is the scene-by-scene script, with the source of every number on screen.

## Where the content comes from

- Numbers: the scorecard (version 75), built from `docs/results` by `docs/playbook/templates/scorecard_page/build_page.py`.
- King's messages and what Claude did next: `docs/playbook/records/interactions.json` (via `make_ix.py`).
- The page shots inside the films are captures of the real scorecard and casebook, built locally (`cap/`).

## Rebuilding

From this folder, with the repository's `.venv` and the pre-installed Playwright:

```bash
mkdir -p pages shots out
python ../../docs/playbook/templates/scorecard_page/build_page.py pages/scorecard.html
cp ../../docs/playbook/templates/casebook_page/casebook.html pages/
python make_ix.py ../../docs/playbook/records/interactions.json ix.js
node cap/cap_sc.js pages/scorecard.html shots "sc_small|#small|1000" "sc_cases|h3:has-text('What the two cases looked like')|1500"
node cap/cap2.js pages/scorecard.html shots cap/specs2_sc.json
node cap/cap2.js pages/scorecard.html shots cap/specs2b.json
node cap/cap2.js pages/casebook.html shots cap/specs2_cb.json
# music
(cd music && python music1.py ../out/music1_full.wav)
(cd music && python music1.py ../out/music1_cut.wav 34.6667 cut)
node render/timeline.js film2.html out/film2_timeline.json
(cd music && python music2.py ../out/film2_timeline.json ../out/music2_full.wav)
# picture, in chunks (frames f0..f1 at 24 fps), then join, denoise, encode and normalise loudness
node render/render.js film1.html out/f1_a.mp4 0 1184 & node render/render.js film1.html out/f1_b.mp4 1184 2368 & wait
render/finish.sh out/film1.mp4 out/music1_full.wav 98.6667 out/f1_a.mp4 out/f1_b.mp4
```

The short cut renders in two parts (`film1cut.html?part=A`, frames 0 to 712; `?part=B`, frames 0 to 136),
joined with an ffmpeg `xfade` of 0.667 s at 29.0 s, then `finish.sh` with `music1_cut.wav` and 34.6667 s.
Film 2 is 8,000 frames; render it in four chunks of 2,000.

## Checks before sending

- `node render/stills.js <page> <dir> t1 t2 ...` renders single frames for a contact sheet.
- `qa/jumps.py film.mp4 outdir`: sudden picture jumps (none over 15 in any of the three films).
- `qa/sound.py film.mp4 accents`: loud jumps, silent holes and the end level. Loudness: `ffmpeg -i film.mp4 -af ebur128=peak=true -f null -`
  (all three: -14 LUFS, true peak -2 dBFS).
- First and last frames are the same poster, so each film also works as a slide.
- Every number on screen is checked against `scripts.md`'s sources.
