#!/usr/bin/sh

FOLD_TO=1048583
BYTES_PER_RECORD=4

BYTES_PER_FEATURE=$(( 2 * BYTES_PER_RECORD ))

FILE_SIZE=$(( FOLD_TO * BYTES_PER_FEATURE ))

dd if=/dev/zero of="$1" bs=$FILE_SIZE count=1 status=progress
