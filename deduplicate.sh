#!/usr/bin/env bash

for file in *.m3u; do
	(echo "#EXTM3U"; cat "$file" | sed 's/#.*//' | sort -u) > tmp.m3u
	mv tmp.m3u "$file" -f
done
