#!/usr/bin/python3
from pprint import pprint

from path_generator import *

goto_points = [
    (65, 65),
    (120, 184),
    (80, 232),
    (56, 232),
    (87, 240),
    (87, 263),
    (87, 240),
    (135, 199),
]

reflect_goto_points = reflect_points(goto_points, True)
goto_points = combine_and_dedupe(goto_points, reflect_goto_points)

def print_goto_points():
    pprint(goto_points)

udp_targets = [
    [(60, 60), (45, 104), (104, 45)],
    [(115, 119), (200, 206), (98, 216)],
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

def print_udp_targets():
    pprint(udp_targets)

assert len(goto_points) == len(udp_targets)

respawn_paths = [
    ([], 0),
    ([], 0),
    ([], 0),
    ([], 1),
    ([], 4),
    ([(52, 247)], 3),
    ([], 2),
    ([], 2),
]

reflect_respawn_paths = []

for path in respawn_paths:
    new_path = (reflect_points(path[0], True), path[1] + len(goto_points) // 2)
    reflect_respawn_paths.append(new_path)

reflect_respawn_paths.reverse()

respawn_paths += reflect_respawn_paths

def print_respawn_paths():
    for i, path in enumerate(respawn_paths):
        print(i, str(path[0]).ljust(8), path[1], goto_points[path[1]], sep='\t')

assert len(respawn_paths) == len(HOST_INDEX_TO_POINTS)

if __name__ == '__main__':
    print(generate(goto_points, udp_targets, respawn_paths), end='')
