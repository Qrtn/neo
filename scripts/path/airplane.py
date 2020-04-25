#!/usr/bin/python

goto_points_1 = [
    (55, 55),
    (120, 184),
    (80, 232),
    (56, 232),
    (87, 240),
    (87, 263),
    (87, 240),
    (135, 199),
    (264, 264),
]

MAX_BOARD_XY = 319

def reflect_points(points):
    return [(MAX_BOARD_XY - p[0], MAX_BOARD_XY - p[1]) for p in points]

def complete_points(points):
    reflected = reflect_points(points)

    if points[-1] == reflected[0]:
        reflected.pop(0)

    if reflected[-1] == points[0]:
        reflected.pop(-1)

    return points + reflected

goto_points = complete_points(goto_points_1)
print(goto_points)
