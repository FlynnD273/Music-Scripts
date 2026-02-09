#!/usr/bin/env bash

dir="${1:-.}"

while read -r path; do
	mp3gain -r -a "$path"
done < <(find "$dir" -name "*.mp3")
