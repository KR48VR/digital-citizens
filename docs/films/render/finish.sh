#!/bin/bash
# finish.sh out.mp4 music.wav seconds chunk1.mp4 chunk2.mp4 ...
# Joins the chunks, light denoise, final encode, music loudness-normalised (two passes, -14 LUFS, true peak -2).
set -e
OUT=$1; WAV=$2; SECS=$3; shift 3
TMP=$(mktemp -d)
for c in "$@"; do echo "file '$(realpath $c)'" >> $TMP/list.txt; done
ffmpeg -y -loglevel error -f concat -safe 0 -i $TMP/list.txt -c copy $TMP/joined.mp4
ffmpeg -y -loglevel error -i $WAV -t $SECS $TMP/m.wav
J=$(ffmpeg -hide_banner -i $TMP/m.wav -af loudnorm=I=-14:TP=-2:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
gv() { echo "$J" | python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }
AF="loudnorm=I=-14:TP=-2:LRA=11:measured_I=$(gv input_i):measured_TP=$(gv input_tp):measured_LRA=$(gv input_lra):measured_thresh=$(gv input_thresh):offset=$(gv target_offset):linear=true,aresample=48000"
ffmpeg -y -loglevel error -i $TMP/joined.mp4 -i $TMP/m.wav -map 0:v -map 1:a -vf "hqdn3d=4:3:6:4.5" -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -movflags +faststart \
  -af "$AF" -c:a aac -b:a 192k -t $SECS $OUT
rm -rf $TMP
ffprobe -v error -show_entries format=duration,size -of default=nw=1 $OUT
