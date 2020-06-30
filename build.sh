#!/bin/sh

set -e

if [ -d "bin" ]; then
    rm -rf bin
fi

mkdir -p bin/vc bin/cf

for tool in vc/sbph vc/ngram vc/bow; do
    cc src/"$tool".c src/vc/vcutils.c -Wall -o bin/"$tool"
done
cc src/cf/nbc.c src/cf/cfutils.c -Wall -o bin/cf/nbc

cp src/cfgparse.py src/dataproc.py src/glue.py src/ml.py src/msapi.py \
   src/msg.py src/stopword.py src/verinfo.py bin/

chmod +x utils/mknbcdat.sh bin/glue.py
