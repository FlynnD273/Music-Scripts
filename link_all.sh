#!/usr/bin/env bash

for file in *.sh *.py; do
	if [ "$file" == "link_all.sh" ]; then
		continue
	fi
	ln -s "../Music-Scripts/$file" "../Music/$file"
done
