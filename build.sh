#!/usr/bin/sh

if [ -d "bin" ]; then
    rm -rf bin
fi

mkdir bin
mkdir bin/cf
mkdir bin/vc
mkdir bin/utils

cc src/cf/nbc.c cf/cfutils.c -lm -Wall -o bin/cf/nbc

cc src/vc/sbph.c vc/vcutils.c -Wall -o bin/vc/sbph
cc src/vc/ngram.c vc/vcutils.c -Wall -o bin/vc/ngram
cc src/vc/bow.c vc/vcutils.c -Wall -o bin/vc/bow

cp src/utils/mknbcdat.sh bin/utils/mknbcdat.sh
cp src/utils/ms.py bin/utils/ms.py
cp src/utils/config.py bin/utils/config.py
cp src/utils/stopword.py bin/utils/stopword.py

chmod +x bin/utils/mknbcdat.sh
chmod +x bin/utils/ms.py
