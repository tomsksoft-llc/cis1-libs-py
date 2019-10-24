#!/bin/bash

ARTIFACTS_DIR=$1

mkdir $ARTIFACTS_DIR

while read file; do
    echo "Copying $file in $ARTIFACTS_DIR"
    cp $file $ARTIFACTS_DIR/$file
done <package.txt

echo "Package built successfully"
