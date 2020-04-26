#!/usr/bin/python3
import copy
from pprint import pprint

from puzzle_general import toggle_lights, chase_lights, check_solution, \
    toggle_row_lights, combine_boards, get_blank_board

from generate_lookup import generate_puzzle_lookup_array, \
    generate_dim_id_lookup_array, encode_puzzle_row, decode_row, \
    generate_top_rows

puzzle_table = generate_puzzle_lookup_array()
dim_id_table = generate_dim_id_lookup_array()

def solve_by_lookup(puzzle_dim, board):
    board = copy.deepcopy(board)

    first_presses, bottom_row = chase_lights(puzzle_dim, board)

    board = get_blank_board(puzzle_dim)
    board[-1] = bottom_row

    puzzle_bits = encode_puzzle_row(puzzle_dim, bottom_row)

    top_row_bits = puzzle_table[puzzle_bits]
    top_row = decode_row(puzzle_dim, top_row_bits)

    #print(puzzle_dim, 'bottom row: ', bottom_row, 'top row: ', top_row)

    top_presses = get_blank_board(puzzle_dim)
    top_presses[0] = top_row

    toggle_row_lights(puzzle_dim, board, 0, top_row)

    second_presses, bottom_row = chase_lights(puzzle_dim, board)
    assert all(i == 0 for i in bottom_row)

    board = get_blank_board(puzzle_dim)
    board[-1] = bottom_row

    presses = combine_boards(puzzle_dim, first_presses, top_presses,
        second_presses)

    return presses


if __name__ == '__main__':
    from example_puzzles import puzzles
    import solve

    ac = True

    for puzzle in puzzles:
        lookup_soln = solve_by_lookup(*puzzle)
        real_soln = solve.solve(*puzzle)

        correct = check_solution(*puzzle, lookup_soln)

        if correct:
            print('Correct')
        else:
            print('Incorrect')
            ac = False

    if ac:
        print('All correct')
