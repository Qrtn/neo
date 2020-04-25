MAX_BOARD_XY = 319

def reflect_points(points, rotational):
    if rotational:
        return [(MAX_BOARD_XY - p[0], MAX_BOARD_XY - p[1]) for p in points]
    else:
        return [(MAX_BOARD_XY - p[1], MAX_BOARD_XY - p[0]) for p in points]

def combine_and_dedupe(left, right):
    l = list(left)
    r = list(right)

    if l[-1] == r[0]:
        l.pop(-1)

    if r[-1] == l[0]:
        r.pop(-1)

    return l + r

def complete_points(points, x_pos, dedupe=True):
    reflected = reflect_points(points, x_pos)

    if dedupe:
        if points[-1] == reflected[0]:
            reflected.pop(0)

        if reflected[-1] == points[0]:
            reflected.pop(-1)

    return points + reflected

HOST_INDEX_TO_TILE_COORDS = {
    # Top-left
    0:  [7, 7],
    1:  [5, 13],
    2:  [13, 5],
    3:  [14, 14],
    # Bottom-left
    4:  [2, 26],
    5:  [6, 33],
    6:  [12, 27],
    7:  [13, 37],
    # Top-right
    8:  [26, 2],
    9:  [27, 12],
    10: [33, 6],
    11: [37, 13],
    # Bottom-right
    12: [25, 25],
    13: [26, 34],
    14: [34, 26],
    15: [32, 32],
}
