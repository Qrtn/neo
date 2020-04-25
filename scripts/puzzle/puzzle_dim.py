#!/usr/bin/python3

import os.path
from collections import namedtuple

puzzle_dir = os.path.dirname(__file__)
puzzle_dim_txt = os.path.join(puzzle_dir, 'puzzle_dimensions.txt')

PuzzleDimension = namedtuple('PuzzleDimension', ['num_rows', 'num_cols',
    'num_colors', 'weight', 'dim_id'], defaults=[None, None])       # weight is not necessary

dimensions = []

with open(puzzle_dim_txt) as f:
    for line_no, line in enumerate(f):
        values = [int(i) for i in line.split()]
        dim = PuzzleDimension(*values, line_no)
        dimensions.append(dim)

def encode_puzzle_dim(dim):
    color_bits = dim.num_colors - 2
    col_bits = (dim.num_cols - 4) << 1
    row_bits = (dim.num_rows - 5) << 3

    return color_bits + col_bits + row_bits

puzzle_dim_bits_to_dim_id = []

for dim in dimensions:
    puzzle_dim_bits = encode_puzzle_dim(dim)
    puzzle_dim_bits_to_dim_id.append((puzzle_dim_bits, dim.dim_id))
