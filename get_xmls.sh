#!/bin/bash

sudo mkdir xmls
FILES=./*
X=0

for f in $FILES;
do
sudo mv $f xmls/;
cd xmls/;
sudo unzip $f;
sudo rm -rf text_000/;
sudo rm -rf native_000/;
cd ..;
X=X+1;
echo "$X / 154";
done

