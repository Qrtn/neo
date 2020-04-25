#!/usr/bin/python3

import sys
import os
import itertools

from puzzle_dim import PuzzleDimension, dimensions, encode_puzzle_dim, \
    puzzle_dim_bits_to_dim_id, dim_id
from puzzle_general import generate_all_rows
import solve

scripts_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(scripts_dir)
import replace_line


ENCODED_ROW_WIDTH = 10
TOP_ROW_DATATYPE = '.short'
DIM_ID_DATATYPE = '.byte'

def encode_row(puzzle_dim, row):
    # Returns 12-bit wide int
    cell_bit_width = 1 if puzzle_dim.num_colors == 2 else 2
    bits = 0

    for i in row:
        bits <<= cell_bit_width
        bits += i

    return bits

def decode_row(puzzle_dim, row_bits):
    cell_bit_width = 1 if puzzle_dim.num_colors == 2 else 2
    cell_mask = 0b1 if cell_bit_width == 1 else 0b11

    row = [0] * puzzle_dim.num_cols

    for bit in range(puzzle_dim.num_cols):
        state = row_bits & cell_mask
        row[-(bit + 1)] = state

        row_bits >>= cell_bit_width

    return row

def encode_puzzle_row(puzzle_dim, bottom_row):
    dim_id_bits = dim_id[puzzle_dim] << ENCODED_ROW_WIDTH
    bottom_row_bits = encode_row(puzzle_dim, bottom_row)

    return dim_id_bits + bottom_row_bits

def generate_top_rows(puzzle_dim):
    top_rows = []

    for bottom_row in generate_all_rows(puzzle_dim):
        try:
            top_row = solve.get_top_row(puzzle_dim, bottom_row)
        except solve.UnsolvablePuzzle:
            continue

        top_rows.append((bottom_row, top_row))

    return top_rows

def generate_puzzle_lookup(puzzle_dims=dimensions):
    lookup_table = []

    for dim in puzzle_dims:
        lookup_by_bottom_row = generate_top_rows(dim)

        for bottom_row, top_row in lookup_by_bottom_row:
            top_row_bits = encode_row(dim, bottom_row)
            full_puzzle_bits = encode_puzzle_row(dim, bottom_row)

            lookup_table.append((full_puzzle_bits, top_row_bits))

    return lookup_table

def list_tuples_to_array(d):
    keys = {i[0] for i in d}

    if len(keys) != len(d):
        raise KeyError("duplicate keys in list of tuples")

    size = max(keys) + 1

    arr = [0] * size
    for key, val in d:
        arr[key] = val

    return arr

def generate_puzzle_lookup_array():
    table = generate_puzzle_lookup()
    return list_tuples_to_array(table)

def generate_dim_id_lookup_array():
    return list_tuples_to_array(puzzle_dim_bits_to_dim_id)

def generate_data_segment(datatype, array):
    return datatype + ' ' + ' '.join(str(i) for i in array)


if __name__ == '__main__':
    USAGE = """\
Example usages:

generate_lookup.py
    Generates lookup table and outputs to stdout

generate_lookup.py -r
    Generates lookup table and replaces respective line in spimbot.s

generate_lookup.py -r <assembly_file>
    Generates lookup table and replaces respective line in <assembly_file>

generate_lookup.py -h
    Prints usage\
    """

    replace = False

    if len(sys.argv) > 1:
        if sys.argv[1] == '-h':
            print(USAGE)
            sys.exit(0)
        elif sys.argv[1] == '-r':
            replace = True

            try:
                asm_filename = sys.argv[3]
            except IndexError:
                scripts_dir = os.path.dirname(__file__)
                asm_filename = os.path.normpath(os.path.join(scripts_dir, '..', 'spimbot.s'))

            if not os.path.exists(asm_filename):
                print('No such file', asm_filename)
                sys.exit(1)

    puzzle_data = generate_data_segment(TOP_ROW_DATATYPE,
        generate_puzzle_lookup_array())

    dim_id_data = generate_data_segment(DIM_ID_DATATYPE,
        generate_dim_id_lookup_array())

    if not replace:
        print(puzzle_data)
        print(dim_id_data)
    else:
        replace_line.replace_in_file(asm_filename, 'puzzle_table:', puzzle_data + '\n')
        replace_line.replace_in_file(asm_filename, 'dim_table:', dim_id_data + '\n')
