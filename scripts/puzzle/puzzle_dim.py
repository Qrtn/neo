#!/usr/bin/python3

from collections import namedtuple

PuzzleDimension = namedtuple('PuzzleDimension', ['num_rows', 'num_cols',
    'num_colors', 'weight'], defaults=[None])       # weight is not necessary

dimensions = []

for line in open('puzzle_dimensions.txt'):
    values = [int(i) for i in line.split()]
    dim = PuzzleDimension(*values)
    dimensions.append(dim)
