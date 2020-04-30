#!/bin/sh

PROJECT_DIR="$(dirname "$0")/.."

$PROJECT_DIR/scripts/path/$1.py > $PROJECT_DIR/build/aml/$2.txt
$PROJECT_DIR/scripts/assemble.py $PROJECT_DIR/build/aml/$2.txt $PROJECT_DIR/build/iml/$2.json
$PROJECT_DIR/scripts/combine.py $PROJECT_DIR/base_spimbot.s $PROJECT_DIR/build/iml/$2.json $PROJECT_DIR/build/puzzle.json $PROJECT_DIR/build/mips/$2.s
