#!/bin/sh

./gen_inst.py $1 | tee /dev/tty | ./replace_line.py ../spimbot.s
