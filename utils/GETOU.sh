#!/bin/bash
ffmpeg -y -i getout.mp3 -t $(echo | awk "{print $RANDOM/32768*$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 getout.mp3)}") GETOU.mp3
