#!/usr/bin/sh

FOLD_TO=8388617
BYTES_PER_RECORD=4

BYTES_PER_FEATURE=$(( 2 * BYTES_PER_RECORD ))
TOTAL_FEATURE_SIZE=$(( FOLD_TO * BYTES_PER_FEATURE ))

# Two additional counter for total numbers of tp/fp.
# Each is 8 bytes.
FILE_SIZE=$(( TOTAL_FEATURE_SIZE + 16 ))

dd if=/dev/zero of="$1" bs=$FILE_SIZE count=1 status=progress
