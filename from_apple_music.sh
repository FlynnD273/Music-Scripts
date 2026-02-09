#!/usr/bin/env bash

shopt -s globstar
for file in **/*.m4a; do
	ffmpeg -i "$file" "${file%.m4a}.mp3" -y
	rm "$file"
done

mv ./* /mnt/tertiary/Music/
