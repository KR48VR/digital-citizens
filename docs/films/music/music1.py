"""Score for Film 1, in film time on the film's bar grid (90 bpm, 4/4; scenes start on bars, see film1.js).
Usage: python music1.py out.wav [seconds] [cut]   ('cut': the 30-second cut's score, on its own bars, see cut.js)"""
import sys
import numpy as np
from synth import Track, pad, pluck, bell, kick, shaker, sub, reverb, write_wav

BAR = 4 * 60 / 90
BEAT = BAR / 4
TOTAL = 37 * BAR
D, Bm, G, A, Em = (50, 54, 57, 62, 64), (47, 54, 59, 62, 66), (43, 55, 59, 62, 67), (45, 57, 61, 64, 69), (40, 55, 59, 64, 67)
# one chord per bar, by scene: poster 0-1, survey 2-4, sort 5-8, shaky 9-14, ai 15-18, blend 19-21, page 22-27,
# honest 28-30, pilot 31-34, end 35-36
CH = [D, D, D, Bm, G, Bm, G, D, A, Bm, Bm, G, G, Em, A, D, A, Bm, G, D, A, G, D, A, Bm, G, D, A, Bm, G, A, G, A, Bm, A, D, D]
SCENE = {'poster': 0, 'survey': 2, 'sort': 5, 'shaky': 9, 'ai': 15, 'blend': 19, 'page': 22, 'honest': 28, 'pilot': 31, 'end': 35}


POPS, BLEND_SPEED, FUND = 4, 1.0, 2


def scene_of(b):
    return max((v, k) for k, v in SCENE.items() if v <= b)[1]


def build(seconds=TOTAL):
    tr = Track(len(CH) * BAR + 4)
    rng = np.random.default_rng(5)
    for b, ch in enumerate(CH):
        t0 = b * BAR
        sc = scene_of(b)
        bass, tones = ch[0], ch[1:]
        # pad: always, softer in the shaky scene (with a tremble) and at the end
        pg = {'poster': 0.5, 'survey': 0.45, 'sort': 0.5, 'shaky': 0.42, 'ai': 0.55, 'blend': 0.6, 'page': 0.5,
              'honest': 0.45, 'pilot': 0.62, 'end': 0.55}[sc]
        if sc == 'end':
            if b == SCENE['end']:  # the last chord: held, then settling to silence on the last frame
                held = (len(CH) - SCENE['end']) * BAR
                tr.add(pad(list(tones) + [74], held - 2.4, attack=0.3, release=2.4, seed=b), t0, 0.62)
                tr.add(sub(bass, held - 2.6, release=2.4), t0, 0.35)
                tr.add(bell(78), t0, 0.22, 0.3)
                tr.add(bell(74), t0 + BEAT * 2, 0.12, -0.3)
            continue
        tr.add(pad(tones, BAR + 0.05, attack=0.5 if b else 1.4, release=1.2, trem=0.35 if sc == 'shaky' else 0, seed=b), t0, pg)
        tr.add(sub(bass, BAR - 0.1), t0, 0.32 if sc not in ('poster', 'shaky') else 0.2)
        arp = [tones[0] + 12, tones[1] + 12, tones[2] + 12, tones[3] + 12]
        if sc == 'poster':
            for k, m in enumerate([tones[2] + 12, tones[3] + 12]):
                tr.add(bell(m), t0 + k * BEAT * 2 + BEAT, 0.12, 0.4 if k else -0.4)
        if sc == 'survey':  # one pluck for every wave of dots popping in
            for k in range(POPS):
                tr.add(pluck(arp[k % 4], 1.4), t0 + k * BAR / POPS, 0.42, (-0.5, 0.5)[k % 2])
        if sc in ('sort', 'page', 'pilot', 'blend'):
            for k in range(8):
                m = arp[(k * 3) % 4] + (12 if k == 7 else 0)
                tr.add(pluck(m, 1.2), t0 + k * BEAT / 2, 0.30 if k % 2 == 0 else 0.2, (-0.4, 0.4)[k % 2])
            for k in (0, 2):
                tr.add(kick(), t0 + k * BEAT, 0.5)
        if sc == 'shaky':  # sparse, uncertain: offbeat plucks, a low pulse from the second bar
            for k in (1, 3):
                tr.add(pluck(arp[k] - 12, 1.8, bright=0.7), t0 + k * BEAT + BEAT / 2, 0.3, 0.3)
            if b >= 10:
                tr.add(kick(), t0, 0.35)
        if sc == 'ai':  # building: 16th-note arpeggio, shaker, kick
            lvl = (b - 15 + 1) / 4
            for k in range(16):
                m = arp[k % 4] + (12 if (k // 4) % 2 else 0)
                tr.add(pluck(m, 0.9, bright=1.3), t0 + k * BEAT / 4, 0.14 + 0.1 * lvl, (-0.6, 0.6)[k % 2])
            for k in range(8):
                tr.add(shaker(seed=int(rng.integers(1 << 30))), t0 + k * BEAT / 2, 0.5 * lvl * (1.3 if k % 2 else 0.8))
            for k in (0, 2):
                tr.add(kick(), t0 + k * BEAT, 0.45 + 0.1 * lvl)
        if sc in ('page', 'pilot'):
            for k in range(8):
                tr.add(shaker(seed=int(rng.integers(1 << 30))), t0 + k * BEAT / 2, 0.35 * (1.3 if k % 2 else 0.8))
        if sc == 'honest':  # pulled back: piano-like plucks on beats 1 and 3
            for k in (0, 2):
                tr.add(pluck(arp[k], 2.2, bright=0.8), t0 + k * BEAT, 0.36, (-0.3, 0.3)[k // 2])
    # accents
    tr.add(bell(81), SCENE['blend'] * BAR + BEAT * 2 / BLEND_SPEED, 0.22, 0.2)   # the marker lands on 3.5
    if 'page' in SCENE:
        tr.add(bell(78), SCENE['page'] * BAR, 0.16, -0.2)                # into the real page
    tr.add(bell(74), SCENE['pilot'] * BAR, 0.18, 0.0)                # the ask
    tr.add(bell(81), (SCENE['pilot'] + FUND) * BAR, 0.2, 0.15)       # 'Fund a pilot.'
    L, R = reverb(tr.L, tr.R)
    n = int(seconds * 48000)
    L, R = L[:n], R[:n]
    # gentle fade at the very end so the last frame is silent
    f = int(0.25 * 48000)
    L[-f:] *= np.linspace(1, 0, f); R[-f:] *= np.linspace(1, 0, f)
    return L, R


if __name__ == '__main__':
    if len(sys.argv) > 3 and sys.argv[3] == 'cut':  # the short cut: same scenes, fewer bars
        CH = [D, D, Bm, G, D, A, Bm, Em, D, A, Bm, D, D]
        SCENE = {'poster': 0, 'survey': 1, 'sort': 3, 'shaky': 5, 'ai': 7, 'blend': 10, 'pilot': 11, 'end': 12}
        TOTAL = len(CH) * BAR
        POPS, BLEND_SPEED, FUND = 6, 2.0, 0
    secs = float(sys.argv[2]) if len(sys.argv) > 2 else TOTAL
    L, R = build(secs)
    write_wav(sys.argv[1], L, R)
    print('wrote', sys.argv[1], round(len(L) / 48000, 2), 's')
