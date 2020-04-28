#!/usr/bin/python3
import sys
from pprint import pprint

from path_generator import *

RED_CLOCKWISE = True

goto_points = [
    (66, 66),
    (120, 191),
    (69, 227),
    (61, 227),
    (69, 227),
    (120, 191),
]

reflect_goto_points = reflect_points(goto_points, True)
goto_points = combine_and_dedupe(goto_points, reflect_goto_points)

if RED_CLOCKWISE:
    goto_points.append(goto_points.pop(0))
    goto_points.reverse()

def print_goto_points():
    pprint(goto_points)

udp_targets = [
    [(63, 63), (43, 104), (104, 43)],
    [(115, 119), (200, 205)],
    [],
    [(23, 213), (49, 264), (109, 296), (96, 220)],
    [],
    [(115, 119), (200, 205)],
]

udp_targets = [sorted(points) for points in udp_targets]

reflect_udp_targets = [sorted(reflect_points(points, True)) for points in
    udp_targets]

udp_targets += reflect_udp_targets

if RED_CLOCKWISE:
    udp_targets.append(udp_targets.pop(0))
    udp_targets.reverse()

def print_udp_targets():
    pprint(udp_targets)

assert len(goto_points) == len(udp_targets)

respawn_paths = [
    # Lower-left triangle
    ([], 0),
    ([(52, 87)], 0),
    ([(87, 52)], 0),
    ([], 1),

    ([], 3),
    ([(52, 247)], 3),
    ([], 3),
    ([(95, 271)], 3),

    # Upper-right triangle
    ([(224, 48)], 9),
    ([], 9),
    ([(267, 72)], 9),
    ([], 9),

    ([], 7),
    ([(232, 267)], 6),
    ([(267, 232)], 6),
    ([], 6),
]

if RED_CLOCKWISE:
    # Converting from CCW restart_at to CW restart_at
    # x -> (n - x) % n
    # 0 -> (n - 0) % n
    # 1 -> n - 1
    # 2 -> n - 2
    # ...
    # n - 1 -> n - (n - 1) = 1

    n = len(goto_points)

    for i in range(len(respawn_paths)):
        extra_visits, restart_at = respawn_paths[i]
        new_restart_at = (n - restart_at) % n
        respawn_paths[i] = (extra_visits, new_restart_at)

def print_respawn_paths():
    for i, path in enumerate(respawn_paths):
        print(i, str(path[0]).ljust(8), path[1], goto_points[path[1]], sep='\t')

assert len(respawn_paths) == len(HOST_INDEX_TO_POINTS)

should_sweep_shoot = [True] * len(goto_points)

def print_sweep_shoot():
    pprint(should_sweep_shoot)

if __name__ == '__main__':
    #print_goto_points()
    #print_udp_targets()
    #print_respawn_paths()

    print('!important! RED_CLOCKWISE is', RED_CLOCKWISE, file=sys.stderr)

    print(generate(goto_points, udp_targets, respawn_paths, should_sweep_shoot), end='')
