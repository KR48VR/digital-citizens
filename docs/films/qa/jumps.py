"""Picture jumps: d = mean abs change between frames (160x90 grey); j = |change in d|. Lists j > 15 and > 25,
and makes a contact sheet of 5 frames around each of the biggest. Usage: python jumps.py film.mp4 outdir"""
import subprocess, sys, numpy as np
from PIL import Image
film, out = sys.argv[1], sys.argv[2]
raw = subprocess.run(['ffmpeg', '-v', 'error', '-i', film, '-vf', 'scale=160:90,format=gray', '-f', 'rawvideo', '-'], capture_output=True).stdout
F = np.frombuffer(raw, np.uint8).reshape(-1, 90, 160).astype(float)
d = np.abs(np.diff(F, axis=0)).mean(axis=(1, 2))
j = np.abs(np.diff(d))
print(f'{len(F)} frames; largest frame change d = {d.max():.1f} at frame {d.argmax() + 1}; largest jump j = {j.max():.1f} at frame {j.argmax() + 1}')
print('jumps over 15:', int((j > 15).sum()), ' over 25:', int((j > 25).sum()))
top = np.argsort(-d)[:8]
print('biggest frame changes (frame, seconds, d):', [(int(i + 1), round((i + 1) / 24, 2), round(float(d[i]), 1)) for i in sorted(top)])
rows = []
for i in sorted(top):
    idx = [max(0, min(len(F) - 1, i + k)) for k in (-1, 0, 1, 2, 3)]
    rows.append(np.hstack([F[x] for x in idx]))
Image.fromarray(np.vstack(rows).astype(np.uint8)).resize((800 * 2, 90 * 2 * len(rows))).save(f'{out}/jumps.png')
