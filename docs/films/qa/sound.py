"""Sound envelope: RMS in 25 ms windows; flags rises/drops > 9 dB within 75 ms, silent holes, the end level.
Usage: python sound.py film.mp4 [accent seconds, comma separated]"""
import subprocess, sys, numpy as np
film = sys.argv[1]
acc = [float(x) for x in sys.argv[2].split(',')] if len(sys.argv) > 2 and sys.argv[2] else []
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', film, '-ac', '1', '-ar', '48000', '-f', 's16le', '-'], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(float) / 32768
w = 1200
n = len(x) // w
rms = np.sqrt((x[:n * w].reshape(n, w) ** 2).mean(axis=1) + 1e-12)
db = 20 * np.log10(rms)
k = 3  # 75 ms
ch = db[k:] - db[:-k]
flags = [(round(i * 0.025, 2), round(float(ch[i]), 1)) for i in range(len(ch)) if abs(ch[i]) > 9 and i * 0.025 > 0.3 and i * 0.025 < len(x) / 48000 - 0.6]
near = lambda t: any(abs(t - a) < 0.15 for a in acc)
print(f'{len(x) / 48000:.2f} s; median level {np.median(db):.1f} dB')
print('rises/drops > 9 dB in 75 ms (not at a listed accent):', [f for f in flags if not near(f[0])][:30])
holes = [round(i * 0.025, 2) for i in range(len(db)) if db[i] < -50 and 1 < i * 0.025 < len(x) / 48000 - 3]
print('silent windows (< -50 dB) away from the start and end:', len(holes), holes[:10])
print(f'last 0.1 s level: {20 * np.log10(np.sqrt((x[-4800:] ** 2).mean()) + 1e-12):.1f} dB')
