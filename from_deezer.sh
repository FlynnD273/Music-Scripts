#!/usr/bin/env bash

shopt -s globstar

in="$1"
out="$2"

for file in "$in"/**/*.mp3; do
	echo $file
	{
		read -r artist 
		read -r album
		read -r band
	} < <(exiftool -s3 -artist -album -band "$file")
	band=${band:-$artist}
	album=${album/\//}
	folder="$out/$band/$album" 
	if [ ! -d "$folder" ]; then
		mkdir -p "$folder"
	fi
	name="$(basename "$file")"
	name="${name#*@}"
	mv "$file" "$folder/$name"
done
