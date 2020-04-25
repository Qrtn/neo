#!/usr/bin/python3
import copy

from puzzle_general import toggle_lights, chase_lights, check_solution, \
    toggle_row_lights

from generate_lookup import generate_puzzle_lookup_array, \
    generate_dim_id_lookup_array, encode_puzzle_row, decode_row, \
    generate_top_rows

puzzle_table = generate_puzzle_lookup_array()
dim_id_table = generate_dim_id_lookup_array()

def solve_by_lookup(puzzle_dim, board):
    board = copy.deepcopy(board)

    _, bottom_row = chase_lights(puzzle_dim, board)
    puzzle_bits = encode_puzzle_row(puzzle_dim, bottom_row)

    top_row_bits = puzzle_table[puzzle_bits]
    top_row = decode_row(puzzle_dim, top_row_bits)

    toggle_row_lights(puzzle_dim, board, 0, top_row)

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
