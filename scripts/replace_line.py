#!/usr/bin/python3
import sys

import fileinput

def replace_in_file(file_path, search_text_prev_line, new_text, once=True):
    with fileinput.input(file_path, inplace=True) as f:
        found = False
        done = False

        for line in f:
            if found and not done:
                print(new_text, end='')
                found = False

                if once:
                    done = True
            else:
                print(line, end='')

            if line.strip() == search_text_prev_line:
                found = True

if __name__ == '__main__':
    filename = sys.argv[1]
    search_text = 'movement:'

    new_text = sys.stdin.read()

    if not new_text:
        new_text = '\n'

    replace_in_file(filename, search_text, new_text)
