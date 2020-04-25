#!/usr/bin/python3
import copy

from generate_lookup import generate_puzzle_lookup_array, \
    generate_dim_id_lookup_array, encode_puzzle_row, decode_row, \
    generate_top_rows

dxy = [
    (0, 0),
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

def toggle_lights(puzzle_dim, board, row, col, times):
    if times % puzzle_dim.num_colors == 0:
        return

    for dx, dy in dxy:
        y = row + dx
        x = col + dy

        if x < 0 or x >= puzzle_dim.num_cols or \
            y < 0 or y >= puzzle_dim.num_rows:
            continue

        board[y][x] = (board[y][x] + times) % puzzle_dim.num_colors

def check_solution(puzzle_dim, board, solution):
    board = copy.deepcopy(board)

    for row_num, row in enumerate(solution):
        for col_num, times in enumerate(row):
            toggle_lights(puzzle_dim, board, row_num, col_num, times)

    for row in board:
        for state in row:
            if state != 0:
                return False

    return True

def chase_lights(puzzle_dim, board):
    presses = [[0] * puzzle_dim.num_cols for i in range(puzzle_dim.num_rows)]

    board = copy.deepcopy(board)
    for row_num, row in enumerate(board[:-1]):
        for col_num, state in enumerate(row):
            if state != 0:
                presses[row_num + 1][col_num] = puzzle_dim.num_colors - state

                toggle_lights(puzzle_dim, board, row_num + 1, col_num,
                    puzzle_dim.num_colors - state)

    bottom_row = board[-1]
    return presses, bottom_row

puzzle_table = generate_puzzle_lookup_array()
dim_id_table = generate_dim_id_lookup_array()

def solve_by_lookup(puzzle_dim, board):
    board = copy.deepcopy(board)

    _, bottom_row = chase_lights(puzzle_dim, board)
    puzzle_bits = encode_puzzle_row(puzzle_dim, bottom_row)

    top_row_bits = puzzle_table[puzzle_bits]
    top_row = decode_row(puzzle_dim, top_row_bits)

    for col, times in enumerate(top_row):
        toggle_lights(puzzle_dim, board, 0, col, times)

    presses, bottom_row = chase_lights(puzzle_dim, board)
    presses[0] = top_row
    print(bottom_row)

    return presses


if __name__ == '__main__':
    from pprint import pprint
    from example_puzzles import puzzles
    import solve

    for puzzle in puzzles:
        lookup_soln = solve_by_lookup(*puzzle)
        real_soln = solve.solve(*puzzle)

        if lookup_soln != real_soln:
            pprint(lookup_soln)
            pprint(real_soln)

        print(check_solution(*puzzle, lookup_soln))

    print('All correct')
