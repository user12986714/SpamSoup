#!/usr/bin/sh

grep 'INSERT INTO `'"$1"'` VALUES' "$2" | sed 's/^INSERT INTO `'"$1"'` VALUES //' | sed 's/;$//'
