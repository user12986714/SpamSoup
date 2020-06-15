#!/usr/bin/sh

if [ -d "bin" ]; then
    rm -rf bin
fi

mkdir bin
mkdir bin/tk
mkdir bin/vc
mkdir bin/cf

cp src/tk/nt.py bin/tk/nt.py
cp src/tk/stopword.py bin/tk/stopword.py

cc src/vc/sbph.c src/vc/vcutils.c -Wall -o bin/vc/sbph
cc src/vc/ngram.c src/vc/vcutils.c -Wall -o bin/vc/ngram
cc src/vc/bow.c src/vc/vcutils.c -Wall -o bin/vc/bow

cc src/cf/nbc.c src/cf/cfutils.c -lm -Wall -o bin/cf/nbc

cp src/ms.py bin/ms.py
cp src/config.json bin/config.json
cp src/verinfo.json bin/verinfo.json

chmod +x utils/mknbcdat.sh

chmod +x bin/ms.py
