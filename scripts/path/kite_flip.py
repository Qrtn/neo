#!/usr/bin/python3
import sys
import copy
from pprint import pprint

from path_generator import *

try:
    INITIAL_CLOCKWISE = (sys.argv[1] == '1')
except IndexError:
    INITIAL_CLOCKWISE = True

MOVING_VEL = 3

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

def flip_goto_points(goto_points):
    goto_points = copy.deepcopy(goto_points)
    goto_points.append(goto_points.pop(0))
    goto_points.reverse()

    return goto_points

if INITIAL_CLOCKWISE:
    goto_points = flip_goto_points(goto_points)

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

if INITIAL_CLOCKWISE:
    udp_targets = flip_goto_points(udp_targets)

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

def flip_respawn_paths(respawn_paths):
    # Converting from CCW restart_at to CW restart_at
    # x -> (n - x) % n
    # 0 -> (n - 0) % n
    # 1 -> n - 1
    # 2 -> n - 2
    # ...
    # n - 1 -> n - (n - 1) = 1
    respawn_paths = copy.deepcopy(respawn_paths)

    n = len(goto_points)

    for i in range(len(respawn_paths)):
        extra_visits, restart_at = respawn_paths[i]
        new_restart_at = (n - restart_at) % n
        respawn_paths[i] = (extra_visits, new_restart_at)

    return respawn_paths

if INITIAL_CLOCKWISE:
    respawn_paths = flip_respawn_paths(respawn_paths)

def print_respawn_paths():
    for i, path in enumerate(respawn_paths):
        print(i, str(path[0]).ljust(8), path[1], goto_points[path[1]], sep='\t')

assert len(respawn_paths) == len(HOST_INDEX_TO_POINTS)

should_sweep_shoot = [True] * len(goto_points)

def print_sweep_shoot():
    pprint(should_sweep_shoot)

# Creating two copies of generated AML

args_original = [goto_points, udp_targets, respawn_paths, should_sweep_shoot, 0, 0, MOVING_VEL]
aml_original = generate(*args_original)

flipped_initial_line_no = len(aml_original.splitlines())
args_flipped = [flip_goto_points(goto_points), flip_goto_points(udp_targets), flip_respawn_paths(respawn_paths), should_sweep_shoot, flipped_initial_line_no, 16, MOVING_VEL]
aml_flipped = generate(*args_flipped)

if __name__ == '__main__':
    #print_goto_points()
    #print_udp_targets()
    #print_respawn_paths()

    print('!important! INITIAL_CLOCKWISE is', INITIAL_CLOCKWISE, file=sys.stderr)

    print(aml_original, end='')
    print(aml_flipped, end='')
