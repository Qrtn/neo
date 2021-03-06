import itertools
import copy

CROSS_DXY = [
    (0, 0),
    (-1, 0),
    (1, 0),
    (0, -1),
    (0, 1)
]

def get_blank_board(puzzle_dim):
    return [[0] * puzzle_dim.num_cols for i in range(puzzle_dim.num_rows)]

def generate_all_rows(puzzle_dim):
    return (list(br) for br in itertools.product(range(puzzle_dim.num_colors),
        repeat=puzzle_dim.num_cols))

def toggle_lights(puzzle_dim, board, row, col, times):
    if times % puzzle_dim.num_colors == 0:
        return

    for dx, dy in CROSS_DXY:
        y = row + dx
        x = col + dy

        if x < 0 or x >= puzzle_dim.num_cols or \
            y < 0 or y >= puzzle_dim.num_rows:
            continue

        board[y][x] = (board[y][x] + times) % puzzle_dim.num_colors

def toggle_row_lights(puzzle_dim, board, row_num, row_toggles):
    for col, times in enumerate(row_toggles):
        toggle_lights(puzzle_dim, board, row_num, col, times)

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
    presses = get_blank_board(puzzle_dim)

    board = copy.deepcopy(board)
    for row_num, row in enumerate(board[:-1]):
        for col_num, state in enumerate(row):
            if state != 0:
                times = puzzle_dim.num_colors - state
                presses[row_num + 1][col_num] = times

                toggle_lights(puzzle_dim, board, row_num + 1, col_num, times)

    bottom_row = board[-1]
    return presses, bottom_row

def combine_boards(puzzle_dim, *boards):
    board = get_blank_board(puzzle_dim)

    for b in boards:
        for i in range(puzzle_dim.num_rows):
            for j in range(puzzle_dim.num_cols):
                board[i][j] += b[i][j]

    for i in range(puzzle_dim.num_rows):
        for j in range(puzzle_dim.num_cols):
            board[i][j] %= puzzle_dim.num_colors

    return board
