#!/usr/bin/python3

import sys
import os
import itertools
import json

from puzzle_dim import PuzzleDimension, dimensions, encode_puzzle_dim, \
    puzzle_dim_bits_to_dim_id, dim_id
from puzzle_general import generate_all_rows
import solve
import generate_top_row

scripts_dir = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(scripts_dir)
import replace_line


ENCODED_ROW_WIDTH = 10
TOP_ROW_DATATYPE = '.half'
DIM_ID_DATATYPE = '.byte'

def encode_row(puzzle_dim, row):
    # Returns 10-bit wide int
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
        row[puzzle_dim.num_cols - 1 - bit] = state

        row_bits >>= cell_bit_width

    return row

def encode_puzzle_row(puzzle_dim, bottom_row):
    dim_id_bits = dim_id[puzzle_dim] << ENCODED_ROW_WIDTH
    bottom_row_bits = encode_row(puzzle_dim, bottom_row)

    return dim_id_bits + bottom_row_bits

def generate_top_rows(puzzle_dim, cpp_get_top_row=False):
    top_rows = []

    get_top_row = solve.get_top_row if cpp_get_top_row else \
        generate_top_row.get_top_row

    for bottom_row in generate_all_rows(puzzle_dim):
        try:
            top_row = get_top_row(puzzle_dim, bottom_row)
        except (solve.UnsolvablePuzzle, IndexError):
            continue

        top_rows.append((bottom_row, top_row))

    return top_rows

def generate_puzzle_lookup(puzzle_dims=dimensions):
    lookup_table = []

    for dim in puzzle_dims:
        lookup_by_bottom_row = generate_top_rows(dim)

        for bottom_row, top_row in lookup_by_bottom_row:
            top_row_bits = encode_row(dim, top_row)
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
    Generates lookup tables and outputs JSON to stdout

generate_lookup.py <output_file>
    Generates lookup tables and outputs JSON to output_file

generate_lookup.py -h
    Prints usage\
    """

    output_filename = None

    try:
        output_filename = sys.argv[1]
    except IndexError:
        pass

    if output_filename == '-h':
        print(USAGE)
        sys.exit(0)

    if output_filename is None:
        output_file = sys.stdout
    else:
        output_file = open(output_filename, 'w')


    puzzle_data = generate_data_segment(TOP_ROW_DATATYPE,
        generate_puzzle_lookup_array())

    dim_id_data = generate_data_segment(DIM_ID_DATATYPE,
        generate_dim_id_lookup_array())


    json = json.dumps({
        'puzzle_data': puzzle_data,
        'dim_id_data': dim_id_data
    }, indent=4)


    with output_file:
        output_file.write(json + '\n')
