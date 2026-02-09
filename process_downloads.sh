#!/usr/bin/env bash

while read -r path; do
	ffmpeg -nostdin -i "$path" -b:a 320K "${path%.flac}.mp3"
done < <(find ~/Downloads -name "*.flac")

/mnt/tertiary/Music/from_deezer.sh ~/Downloads ~/Downloads/Music
/mnt/tertiary/Music/gainall.sh ~/Downloads/Music
python /mnt/tertiary/Music/normalise.py ~/Downloads/Music
