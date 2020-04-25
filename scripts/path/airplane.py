#!/usr/bin/python
from pprint import pprint

MAX_BOARD_XY = 319

def reflect_points(points, x_pos):
    if x_pos:
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

goto_points = [
    (59, 59),
    (120, 184),
    (80, 232),
    (56, 232),
    (87, 240),
    (87, 263),
    (87, 240),
    (135, 199),
    (260, 260),
]

reflect_goto_points = reflect_points(goto_points, True)
goto_points = combine_and_dedupe(goto_points, reflect_goto_points)

pprint(goto_points)

udp_targets = [
    [(60, 60), (45, 104), (104, 45)],
    [(115, 119), (200, 206)],
    [(96, 219), (107, 296)],
    [(23, 211), (96, 220), (50, 264)],
]

udp_targets = [sorted(points) for points in udp_targets]

reflect_udp_targets_1 = [sorted(reflect_points(points, False)) for points in
    udp_targets]

udp_targets += reversed(reflect_udp_targets_1)

# Look at airplane.xcf path for more details
udp_targets[4], udp_targets[5] = udp_targets[5], udp_targets[4]
udp_targets.insert(4, [])

reflect_udp_targets_2 = [sorted(reflect_points(points, True)) for points in
    udp_targets]

udp_targets = combine_and_dedupe(udp_targets, reflect_udp_targets_2)

pprint(udp_targets)

assert len(goto_points) == len(udp_targets)
