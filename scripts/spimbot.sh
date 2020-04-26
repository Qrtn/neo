#!/bin/sh

PROJECT_DIR="$(dirname "$0")/.."

if [ "$#" -eq 0 ]; then
    QtSpimbot -file $PROJECT_DIR/spimbot.s -file2 $PROJECT_DIR/spimbot_slow_solver.s -randommap -randompuzzle
else
    QtSpimbot -file $PROJECT_DIR/spimbot.s -file2 $PROJECT_DIR/spimbot_slow_solver.s $*
fi

