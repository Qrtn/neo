#!/usr/bin/sh

read line
sed "/movement:/!b;n;c$line" $1
