#!/usr/bin/python3

import os.path
from collections import namedtuple

puzzle_dir = os.path.dirname(__file__)
puzzle_dim_txt = os.path.join(puzzle_dir, 'puzzle_dimensions.txt')

PuzzleDimension = namedtuple('PuzzleDimension', ['num_rows', 'num_cols',
    'num_colors'])

dimensions = []

with open(puzzle_dim_txt) as f:
    for line in f:
        values = [int(i) for i in line.split()]
        dim = PuzzleDimension(*values[:-1]) # Don't include weight
        dimensions.append(dim)

def encode_puzzle_dim(dim):
    color_bits = dim.num_colors - 2
    col_bits = (dim.num_cols - 4) << 1
    row_bits = (dim.num_rows - 5) << 3

    return color_bits + col_bits + row_bits

dim_id = {}
puzzle_dim_bits_to_dim_id = []

for i, dim in enumerate(dimensions):
    dim_id[dim] = i

    puzzle_dim_bits = encode_puzzle_dim(dim)
    puzzle_dim_bits_to_dim_id.append((puzzle_dim_bits, i))
