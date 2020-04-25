#!/usr/bin/python3
from puzzle_dim import PuzzleDimension, dimensions

RAW_BOARDS = ["""
 0   1   1   0   1   0
 1   1   0   1   1   1
 0   0   1   0   1   1
 0   1   1   0   1   1
 1   1   1   0   1   0
""","""
 0   2   1
 1   2   2
 1   2   2
 2   2   2
 2   2   1
 2   0   2
 2   2   2
 0   0   0
 2   2   0
 1   0   1
 2   0   0
 2   2   2
 1   1   2
"""]

puzzles = []

for board in RAW_BOARDS:
    rows = board.strip().splitlines()
    board = [[int(i) for i in row.split()] for row in rows]

    num_rows = len(rows)
    num_cols = len(rows[0].split())
    num_colors = max(i for row in board for i in row) + 1

    dim = PuzzleDimension(num_rows, num_cols, num_colors)

    puzzles.append((dim, board))

if __name__ == '__main__':
    from pprint import pprint

    pprint(puzzles)
