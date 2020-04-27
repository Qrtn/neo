#!/usr/bin/python3

import sys
import string
import json


class AtTemplate(string.Template):
    delimiter = '@'

def replace(mips, iml_data, puzzle_data):
    return AtTemplate(mips).safe_substitute(**iml_data, **puzzle_data)


if __name__ == '__main__':
    USAGE = """\
error: invalid number of args

usage:

combine.py <base_spimbot> <iml_file> <puzzle_file>
    Outputs MIPS file to stdout

combine.py <base_spimbot> <iml_file> <puzzle_file> <output_file>
    Outputs MIPS file to output_file"""

    num_args = len(sys.argv) - 1
    if num_args not in (3, 4):
        print(USAGE)
        sys.exit(1)

    base_spimbot, iml_filename, puzzle_filename, *output_filename = sys.argv[1:]

    if output_filename:
        output_file = open(output_filename[0], 'w')
    else:
        output_file = sys.stdout

    base_mips = open(base_spimbot).read()
    iml_data = json.load(open(iml_filename))
    puzzle_data = json.load(open(puzzle_filename))

    output_mips = replace(base_mips, iml_data, puzzle_data)

    with output_file:
        output_file.write(output_mips)
