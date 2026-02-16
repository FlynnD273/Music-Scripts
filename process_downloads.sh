#!/usr/bin/env bash

while read -r path; do
	ffmpeg -nostdin -i "$path" -b:a 320K "${path%.flac}.mp3"
done < <(find ~/Downloads -name "*.flac")

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
$SCRIPT_DIR/from_deezer.sh ~/Downloads ~/Downloads/Music
$SCRIPT_DIR/gainall.sh ~/Downloads/Music
python $SCRIPT_DIR/normalise.py ~/Downloads/Music
