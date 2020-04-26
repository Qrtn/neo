#!/usr/bin/python3

import sys
import os.path

from puzzle_dim import PuzzleDimension, dimensions

puzzle_dir = os.path.dirname(__file__)
example_puzzles_txt = os.path.join(puzzle_dir, 'example_puzzles.txt')

def convert_debug_log_to_example_boards(debug_log):
    lines = debug_log.splitlines()

    raw_boards = []

    capturing_board = False
    board = []

    for line in lines:
        if 'puzzle: generated board:' in line:
            capturing_board = True
        elif 'finished creating puzzle' in line:
            raw_boards.append('\n'.join(board))

            capturing_board = False
            board = []
        elif capturing_board:
            board.append(line)

    return '\n\n'.join(raw_boards) + '\n'

def convert_example_boards_to_puzzles(data):
    data = data.strip()
    if not data:
        return []

    raw_boards = data.split('\n\n')

    puzzles = []

    for board in raw_boards:
        rows = board.strip().splitlines()
        board = [[int(i) for i in row.split()] for row in rows]

        num_rows = len(rows)
        num_cols = len(rows[0].split())
        num_colors = max(i for row in board for i in row) + 1

        dim = PuzzleDimension(num_rows, num_cols, num_colors)

        puzzles.append((dim, board))

    return puzzles


with open(example_puzzles_txt) as f:
    data = f.read()

    puzzles = convert_example_boards_to_puzzles(data)

if __name__ == '__main__':
    from pprint import pprint

    debug_log = sys.stdin.read()
    example_boards = convert_debug_log_to_example_boards(debug_log)
    puzzles = convert_example_boards_to_puzzles(example_boards)

    print(len(puzzles), 'boards added to example_boards.txt')

    if puzzles:
        with open(example_puzzles_txt, 'a') as f:
            f.write('\n')
            f.write(example_boards)
