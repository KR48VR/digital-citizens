"""Small numpy synth for the films' scores: pads, plucks, bells, a soft kick and shaker, and a simple reverb.
Everything is written in film time on a bar grid, so scene changes land on bar lines."""
import numpy as np
from scipy.signal import fftconvolve

SR = 48000


def hz(m):
    return 440.0 * 2 ** ((m - 69) / 12)


class Track:
    def __init__(self, seconds):
        self.n = int(seconds * SR)
        self.L = np.zeros(self.n)
        self.R = np.zeros(self.n)

    def add(self, sig, t0, gain=1.0, pan=0.0):
        i0 = int(t0 * SR)
        if i0 >= self.n:
            return
        sig = sig[: self.n - i0]
        gl, gr = gain * np.cos((pan + 1) * np.pi / 4), gain * np.sin((pan + 1) * np.pi / 4)
        self.L[i0:i0 + len(sig)] += sig * gl * 1.414
        self.R[i0:i0 + len(sig)] += sig * gr * 1.414


def env_adsr(n, a, r, sustain_n):
    e = np.ones(n)
    na, nr = int(a * SR), int(r * SR)
    e[:na] = np.linspace(0, 1, na) ** 2 if na else 1
    rs = min(sustain_n, n)
    if nr and rs < n:
        tail = np.linspace(1, 0, n - rs) ** 2
        e[rs:] *= tail
    return e


def pad(midis, dur, attack=1.2, release=1.8, bright=8, detune=0.004, trem=0.0, seed=0):
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    out = np.zeros(n)
    rng = np.random.default_rng(seed)
    for m in midis:
        f0 = hz(m)
        for d in (-detune, 0, detune):
            ph = rng.uniform(0, 2 * np.pi)
            for h in range(1, bright + 1):
                if f0 * h > 9000:
                    break
                out += np.sin(2 * np.pi * f0 * (1 + d) * h * t + ph * h) / (h ** 1.6)
    out *= env_adsr(n, attack, release, int(dur * SR))
    if trem:
        out *= 1 - trem * 0.5 * (1 + np.sin(2 * np.pi * 5.5 * t))
    return out / (len(midis) * 3 * 1.6)


def pluck(m, dur=1.6, bright=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f0 = hz(m)
    out = np.zeros(n)
    for h in range(1, 9):
        if f0 * h > 12000:
            break
        out += np.sin(2 * np.pi * f0 * h * t) * np.exp(-t * (2.2 + 1.6 * h / bright)) / h ** 1.3
    a = int(0.004 * SR)
    out[:a] *= np.linspace(0, 1, a)
    return out * 0.5


def bell(m, dur=4.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f0 = hz(m)
    out = np.zeros(n)
    for ratio, amp, dec in ((1, 1, 1.0), (2.76, 0.45, 1.8), (5.4, 0.25, 3.0), (8.93, 0.12, 4.5), (2.0, 0.3, 1.2)):
        out += amp * np.sin(2 * np.pi * f0 * ratio * t) * np.exp(-t * dec)
    a = int(0.003 * SR)
    out[:a] *= np.linspace(0, 1, a)
    return out * 0.35


def kick(dur=0.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 46 + 70 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7.5) * 0.9


def shaker(dur=0.09, seed=0):
    n = int(dur * SR)
    rng = np.random.default_rng(seed)
    x = np.diff(rng.standard_normal(n + 1))
    t = np.arange(n) / SR
    return x * np.exp(-t * 55) * 0.08


def sub(m, dur, release=0.4):
    n = int((dur + release) * SR)
    t = np.arange(n) / SR
    out = np.sin(2 * np.pi * hz(m) * t) + 0.25 * np.sin(4 * np.pi * hz(m) * t)
    return out * env_adsr(n, 0.05, release, int(dur * SR)) * 0.5


def reverb(L, R, seconds=2.6, wet=0.28, seed=3):
    rng = np.random.default_rng(seed)
    n = int(seconds * SR)
    t = np.arange(n) / SR
    decay = np.exp(-t * 6.9 / seconds)
    irl = rng.standard_normal(n) * decay
    irr = rng.standard_normal(n) * decay
    # darker tail: smooth the impulse a little
    k = np.ones(12) / 12
    irl, irr = np.convolve(irl, k, 'same'), np.convolve(irr, k, 'same')
    irl /= np.sqrt((irl ** 2).sum()); irr /= np.sqrt((irr ** 2).sum())
    wl = fftconvolve(L, irl)[: len(L)]
    wr = fftconvolve(R, irr)[: len(R)]
    return L * (1 - wet) + wl * wet * 1.0, R * (1 - wet) + wr * wet * 1.0


def write_wav(path, L, R):
    import wave
    peak = max(np.abs(L).max(), np.abs(R).max(), 1e-9)
    L, R = L / peak * 0.89, R / peak * 0.89
    data = np.empty(2 * len(L), dtype=np.int16)
    data[0::2] = (L * 32767).astype(np.int16)
    data[1::2] = (R * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(data.tobytes())
