"""Score for Film 2, in film time on the film's bar grid (90 bpm, 4/4), following the exported timeline
(out/film2_timeline.json): every chapter card, page and lesson starts on a bar or half bar.
Usage: python music2.py timeline.json out.wav"""
import json
import sys
import numpy as np
from synth import Track, pad, pluck, bell, kick, shaker, sub, reverb, write_wav

T = json.load(open(sys.argv[1]))
BAR = T['timeline']['bar']
BEAT = BAR / 4
OPEN, CLOSE = T['timeline']['open'], T['timeline']['close']
NBARS = int(round(CLOSE['stop']))
D, Bm, G, A, Em = (50, 54, 57, 62, 64), (47, 54, 59, 62, 66), (43, 55, 59, 62, 67), (45, 57, 61, 64, 69), (40, 55, 59, 64, 67)
PROGS = {'open': [D, G, Bm, A], 0: [D, A, Bm, G], 1: [Bm, G, D, A], 2: [G, D, A, Bm], 3: [Em, G, D, A], 4: [D, Bm, G, A], 'close': [G, A, Bm, A]}


def section(bt):
    """what is on screen at bar position bt (in bars)"""
    if bt < OPEN['timeline']:
        return 'poster', 'open', 0
    if bt < OPEN['ch']:
        name = 'timeline' if bt < OPEN['kinds'] else 'kinds' if bt < OPEN['roles'] else 'roles'
        return name, 'open', OPEN['timeline']
    if bt >= CLOSE['close']:
        name = 'end' if bt >= CLOSE['end'] else 'recap' if bt >= CLOSE['recap'] else 'close'
        return name, 'close', CLOSE['close']
    for b in T['timeline']['beats']:
        if b['a'] <= bt < b['b']:
            return b['type'], b['ch'], b['a']
    return 'ex', 0, 0


def build():
    tr = Track(NBARS * BAR + 4)
    rng = np.random.default_rng(9)
    starts = {(b['ch'], b['type'], b['a']) for b in T['timeline']['beats']}
    for hb in range(NBARS * 2):  # half bars, so beats that start mid-bar get their own accent
        bt = hb / 2
        t0 = bt * BAR
        typ, ch, s0 = section(bt)
        prog = PROGS[ch]
        chord = prog[int(bt) % 4] if ch in ('open', 'close') else prog[int(bt - CHAPTER_START[ch]) % 4]
        bass, tones = chord[0], chord[1:]
        arp = [m + 12 for m in tones]
        whole = hb % 2 == 0
        if typ == 'end':
            if bt == CLOSE['end']:
                dur = (CLOSE['stop'] - CLOSE['end']) * BAR - 2.6
                tr.add(pad(list(D[1:]) + [74], dur, attack=0.4, release=2.4, seed=hb), t0, 0.6)
                tr.add(sub(D[0], dur, release=2.4), t0, 0.32)
                tr.add(bell(78), t0, 0.2, 0.3)
                tr.add(bell(74), t0 + 2 * BEAT, 0.1, -0.3)
            continue
        level = {'poster': 0.5, 'timeline': 0.45, 'kinds': 0.5, 'roles': 0.5, 'card': 0.55, 'ex': 0.4, 'montage': 0.42,
                 'claude': 0.4, 'page': 0.46, 'lesson': 0.6, 'close': 0.5, 'recap': 0.6}[typ]
        tr.add(pad(tones, BAR / 2 + 0.05, attack=0.35 if t0 else 1.2, release=1.0, seed=hb), t0, level)
        if whole:
            tr.add(sub(bass, BAR - 0.1), t0, 0.26)
        # beat starts: a bell on chapter cards and lessons, a soft one on pages
        if bt == s0 and typ in ('card', 'lesson'):
            tr.add(bell(arp[2] + 12 if typ == 'card' else arp[3] + 12), t0, 0.2, 0.2)
        if bt == s0 and typ == 'page':
            tr.add(bell(arp[1] + 12), t0, 0.11, -0.2)
        if typ in ('poster',):
            if whole:
                tr.add(bell(arp[2] + 12), t0 + BEAT, 0.1, 0.4)
        elif typ == 'timeline':  # a pluck on every beat as the dots pop in
            for k in range(2):
                tr.add(pluck(arp[(hb * 2 + k) % 4], 1.3), t0 + k * BEAT, 0.36, (-0.5, 0.5)[k])
        elif typ in ('kinds', 'roles', 'page', 'close', 'recap', 'lesson'):
            for k in range(4):
                m = arp[(k * 3 + hb) % 4] + (12 if typ in ('lesson', 'recap') and k == 3 else 0)
                tr.add(pluck(m, 1.2), t0 + k * BEAT / 2, 0.24 if k % 2 == 0 else 0.15, (-0.4, 0.4)[k % 2])
            if typ in ('page', 'close', 'recap', 'roles'):
                tr.add(kick(), t0, 0.36)
                for k in range(4):
                    tr.add(shaker(seed=int(rng.integers(1 << 30))), t0 + k * BEAT / 2, 0.22 * (1.3 if k % 2 else 0.8))
        elif typ in ('ex', 'montage', 'claude', 'card'):  # reading time: sparse and calm
            if not whole:
                tr.add(pluck(arp[hb % 4] - 12, 1.8, bright=0.7), t0 + BEAT / 2, 0.22, 0.3)
            else:
                tr.add(pluck(arp[(hb // 2) % 4], 2.0, bright=0.8), t0, 0.18, -0.3)
    L, R = reverb(tr.L, tr.R, seconds=2.8, wet=0.3)
    n = int(T['duration'] * 48000)
    L, R = L[:n], R[:n]
    f = int(0.25 * 48000)
    L[-f:] *= np.linspace(1, 0, f); R[-f:] *= np.linspace(1, 0, f)
    return L, R


CHAPTER_START = {}
for b in T['timeline']['beats']:
    CHAPTER_START.setdefault(b['ch'], b['a'])

if __name__ == '__main__':
    L, R = build()
    write_wav(sys.argv[2], L, R)
    print('wrote', sys.argv[2], round(len(L) / 48000, 2), 's')
