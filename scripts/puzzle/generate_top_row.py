#!/usr/bin/python3

import itertools
from collections import defaultdict
from pprint import pprint

import random

from puzzle_dim import dimensions
from puzzle_general import *

def generate_top_rows(puzzle_dim):
    top_row_toggles = defaultdict(list)

    for top_row in generate_all_rows(puzzle_dim):
        board = get_blank_board(puzzle_dim)

        toggle_row_lights(puzzle_dim, board, 0, top_row)

        _, bottom_row = chase_lights(puzzle_dim, board)

        top_row_presses = [(puzzle_dim.num_colors - i) % puzzle_dim.num_colors
            for i in top_row]

        top_row_toggles[tuple(bottom_row)].append(top_row_presses)

    return top_row_toggles

def generate_puzzle_top_rows(puzzle_dims=dimensions):
    puzzle_top_rows = {}

    for puzzle in puzzle_dims:
        puzzle_top_rows[puzzle] = generate_top_rows(puzzle)

    return puzzle_top_rows

puzzle_top_rows = generate_puzzle_top_rows()

def get_top_row(puzzle_dim, bottom_row):
    return puzzle_top_rows[puzzle_dim][tuple(bottom_row)][0]

if __name__ == '__main__':
    for dim in dimensions:
        if dim.num_rows == 5 and dim.num_cols == 6:
            break

    print(puzzle_top_rows[dim][(0, 1, 1, 0, 0, 0)])
