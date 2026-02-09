#!/usr/bin/env bash

find *.m3u -exec sed -E "s/(.*\/Music\/)|(\.\/)//" {} -i \;
