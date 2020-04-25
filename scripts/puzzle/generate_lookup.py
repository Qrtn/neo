#!/usr/bin/python3

import itertools
from puzzle_dim import PuzzleDimension, dimensions, encode_puzzle_dim
import solve

ENCODED_ROW_WIDTH = 10

def encode_row(puzzle_dim, row):
    # Returns 12-bit wide int
    cell_bit_width = 1 if puzzle_dim.num_colors == 2 else 2
    bits = 0

    for i in row:
        bits += i
        bits <<= cell_bit_width

    return bits

def generate_bottom_rows(puzzle_dim):
    return itertools.product(range(puzzle_dim.num_colors),
        repeat=puzzle_dim.num_cols)

def generate_top_rows(puzzle_dim):
    top_rows = []

    for bottom_row in generate_bottom_rows(puzzle_dim):
        try:
            top_row = solve.get_top_row(puzzle_dim, bottom_row)
        except solve.UnsolvablePuzzle:
            continue

        top_rows.append((bottom_row, top_row))

    return top_rows

def generate_puzzle_lookup(puzzle_dims=dimensions):
    lookup_table = []

    for dim in puzzle_dims:
        dim_id_bits = dim.dim_id << ENCODED_ROW_WIDTH

        lookup_by_bottom_row = generate_top_rows(dim)

        for bottom_row, top_row in lookup_by_bottom_row:
            bottom_row_bits = encode_row(dim, bottom_row)
            top_row_bits = encode_row(dim, bottom_row)

            full_puzzle_bits = dim_id_bits + bottom_row_bits

            lookup_table.append((full_puzzle_bits, top_row_bits))

    return lookup_table
