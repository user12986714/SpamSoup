#!/bin/sh

set -e

if [ -d "bin" ]; then
    rm -rf bin
fi
mkdir -p bin/vc bin/cf

# Please don't try to concatenate these lines,
# as those source code may have different dependencies
cc src/vc/sbph.c src/vc/vcutils.c -Wall -o bin/vc/sbph
cc src/vc/ngram.c src/vc/vcutils.c -Wall -o bin/vc/ngram
cc src/vc/bow.c src/vc/vcutils.c -Wall -o bin/vc/bow

cc src/cf/nbc.c src/cf/cfutils.c -lm -Wall -o bin/cf/nbc

# Prepare glueware
cp src/*.py bin/
chmod +x bin/glue.py
