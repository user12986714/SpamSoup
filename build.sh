#!/usr/bin/sh

if [ -d "bin" ]; then
    rm -rf bin
fi

mkdir bin
mkdir bin/vc
mkdir bin/cf

cc src/vc/sbph.c src/vc/vcutils.c -Wall -o bin/vc/sbph
cc src/vc/ngram.c src/vc/vcutils.c -Wall -o bin/vc/ngram
cc src/vc/bow.c src/vc/vcutils.c -Wall -o bin/vc/bow

cc src/cf/nbc.c src/cf/cfutils.c -lm -Wall -o bin/cf/nbc

cp src/cfgparse.py bin/cfgparse.py
cp src/dataproc.py bin/dataproc.py
cp src/glue.py bin/glue.py
cp src/ml.py bin/ml.py
cp src/msapi.py bin/msapi.py
cp src/msg.py bin/msg.py
cp src/stopword.py bin/stopword.py
cp src/verinfo.py bin/verinfo.py

chmod +x utils/mknbcdat.sh

chmod +x bin/glue.py
