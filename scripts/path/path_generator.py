MAX_BOARD_XY = 319

HOST_INDEX_TO_TILE_COORDS = {
    # Top-left
    0:  (7, 7),
    1:  (5, 13),
    2:  (13, 5),
    3:  (14, 14),
    # Bottom-left
    4:  (2, 26),
    5:  (6, 33),
    6:  (12, 27),
    7:  (13, 37),
    # Top-right
    8:  (26, 2),
    9:  (27, 12),
    10: (33, 6),
    11: (37, 13),
    # Bottom-right
    12: (25, 25),
    13: (26, 34),
    14: (34, 26),
    15: (32, 32),
}

HOST_INDEX_TO_POINTS = {
    index: (point[0] * 8 + 4, point[1] * 8 + 4) for index, point in \
        HOST_INDEX_TO_TILE_COORDS.items()
}

GENERATOR_HEADER = [
    '### Generated by path_generator.py ###',
] + [''] * 2

COPY_TIMES = 11

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

def generate(goto_points, udp_targets, respawn_paths):
    lines = GENERATOR_HEADER.copy()
    section_linenos = []

    lines.append('# Main section (executes on initial spawn)')

    for point, targets in zip(goto_points, udp_targets):
        section_linenos.append(len(lines) + 1)

        section_lines = []

        goto = 'goto {} {}'.format(*point)
        section_lines.append(goto)

        for target in targets:
            chkshoot = 'chkshoot {} {}'.format(*target)
            section_lines.append(chkshoot)

        lines += section_lines

    start_of_main = section_linenos[0]
    end_of_main = len(lines)

    main_copy = '!!copy {} {} {}'.format(COPY_TIMES, start_of_main,
        end_of_main)
    lines.append(main_copy)

    # Main section done
    lines += ['']

    for host_index, path in enumerate(respawn_paths):
        section_lines = []

        extra_visits, restart_at_index = path

        restart_at_line = section_linenos[restart_at_index]

        section_header = '# Host index {} at ({}, {})'.format(host_index,
            *HOST_INDEX_TO_POINTS[host_index])
        section_respawn = '!respawn {}'.format(host_index)

        section_lines += [section_header, section_respawn]

        for point in extra_visits:
            goto = 'goto {} {}'.format(*point)
            section_lines.append(goto)

        if restart_at_line > start_of_main:
            section_copy = '!!copy {} {} {} {} {}'.format(COPY_TIMES,
                restart_at_line, end_of_main, start_of_main,
                restart_at_line - 1)
        else:
            section_copy = '!!copy {} {} {}'.format(COPY_TIMES,
                start_of_main, end_of_main)

        section_lines.append(section_copy)

        lines += section_lines

        lines += ['']

    lines += ['', '### End of path_generator.py output ###']

    return '\n'.join(lines) + '\n'

def write_to_file(output, filename):
    with open(filename, 'w') as f:
        f.write(output)

def generate_file(goto_points, udp_targets, respawn_paths, filename):
    output = generate(goto_points, udp_targets, respawn_paths)
    write_to_file(output, filename)
