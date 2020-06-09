#!/usr/bin/sh

DIR="bin"

if [ -d "$DIR" ]; then
    rm -rf $DIR
fi

mkdir $DIR
mkdir $DIR/cf
mkdir $DIR/vc

cc cf/nbc.c cf/cfutils.c -Wall -o $DIR/cf/nbc

cc vc/sbph.c vc/vcutils.c -Wall -o $DIR/vc/sbph
cc vc/ngram.c vc/vcutils.c -Wall -o $DIR/vc/ngram
cc vc/bow.c vc/vcutils.c -Wall -o $DIR/vc/bow
