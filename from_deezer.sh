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
		read -r partofset
	} < <(exiftool -s3 -artist -album -band -partofset "$file")
	band=${band:-$artist}
	album=${album/\//}
	if [[ "$partofset" =~ .*/.* ]] && [[ ! "$partofset" =~ .*/1 ]]; then
		partofset=${partofset%/*}
		partofset=$((partofset+0))
		folder="$out/$band/$album/CD${partofset}" 
	else
		folder="$out/$band/$album" 
	fi
	if [ ! -d "$folder" ]; then
		mkdir -p "$folder"
	fi
	name="$(basename "$file")"
	name="${name#*@}"
	mv "$file" "$folder/$name"
done
