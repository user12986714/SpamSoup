#!/usr/bin/sh

FOLD_TO=67108957
BYTES_PER_RECORD=1

FILE_SIZE=$(( FOLD_TO * BYTES_PER_RECORD ))

head /dev/zero -c $FILE_SIZE | tr '\000' '\001' > "$1"
