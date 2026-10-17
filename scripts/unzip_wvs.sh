#!/usr/bin/env bash
# Unzip every WVS zip under data/raw/wvs into a folder of the same name (idempotent).
cd "$(dirname "$0")/../data/raw/wvs" || exit 1
for z in *.zip; do d="${z%.zip}"; [ -d "$d" ] || unzip -o -q "$z" -d "$d"; done
ls -d */ | wc -l
