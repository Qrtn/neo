#!/bin/sh

PROJECT_DIR="$(dirname "$0")/.."
PATH_SCHEMA="$PROJECT_DIR/scripts/path/$1.py"

if [ -f $PATH_SCHEMA ]; then
    # If path exists then generate aml from it
    $PATH_SCHEMA > $PROJECT_DIR/build/aml/$2.txt
fi

$PROJECT_DIR/scripts/assemble.py $PROJECT_DIR/build/aml/$2.txt $PROJECT_DIR/build/iml/$2.json
$PROJECT_DIR/scripts/combine.py $PROJECT_DIR/base_spimbot.s $PROJECT_DIR/build/iml/$2.json $PROJECT_DIR/build/puzzle.json $PROJECT_DIR/build/mips/$2.s
