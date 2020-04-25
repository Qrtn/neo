#!/usr/bin/python3

import os
import subprocess

CPP_SOLVE = os.path.join(os.path.dirname(__file__), 'cpp_solve', 'solve')

def solve(puzzle_dim, board):
    params = [puzzle_dim.num_rows, puzzle_dim.num_cols,
        puzzle_dim.num_colors]

    for row in board:
        params.extend(row)

    stdin = ' '.join(str(i) for i in params) + '\n'
    stdin = stdin.encode('utf-8')

    proc = subprocess.run(CPP_SOLVE, input=stdin, check=True, capture_output=True)
    output = proc.stdout

    solution_1d = [int(i) for i in output.split()]
    # Group by rows of length num_cols
    solution = [solution_1d[i:i + puzzle_dim.num_cols]
        for i in range(0, len(solution_1d), puzzle_dim.num_cols)]

    return solution


def get_top_row(puzzle_dim, bottom_row):
    assert len(bottom_row) == puzzle_dim.num_cols

    # zero array of size (num_rows - 1) * num_cols
    board = [[0] * puzzle_dim.num_cols for i in range(puzzle_dim.num_rows - 1)]

    board.append(bottom_row)

    solution = solve(puzzle_dim, board)

    return solution[0]

if __name__ == '__main__':
    from pprint import pprint
    from example_puzzles import puzzles

    pprint(solve(*puzzles[0]))
    pprint(get_top_row(puzzles[0][0], puzzles[0][1][-1]))
