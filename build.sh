#!/bin/sh

set -e

if [ -d "bin" ]; then
    rm -rf bin
fi
mkdir -p bin/vc bin/cf

CC="cc"
CCFLAGS="-Wall -O3 -Ofast"

# Please don't try to concatenate these lines,
# as those source code may have different dependencies
$CC src/vc/sbph.c src/vc/vcutils.c $CCFLAGS -o bin/vc/sbph
$CC src/vc/ngram.c src/vc/vcutils.c $CCFLAGS -o bin/vc/ngram
$CC src/vc/bow.c src/vc/vcutils.c $CCFLAGS -o bin/vc/bow
$CC src/vc/osb.c src/vc/vcutils.c $CCFLAGS -o bin/vc/osb
$CC src/vc/sbphmh.c src/vc/vcutils.c $CCFLAGS -o bin/vc/sbphmh

$CC src/cf/nbc.c -lm $CCFLAGS -o bin/cf/nbc
$CC src/cf/winnow.c -lm $CCFLAGS -o bin/cf/winnow

# Prepare glueware
cp src/*.py bin/
chmod +x bin/glue.py
