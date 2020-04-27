#!/usr/bin/python3

# assemble.py: Converts AML to IML JSON

### Movement Pattern
# -360 to 360		absolute angle
# 1500 +- v		velocity
# 2000			UDP, may be contingent on previous check of arena map
# 3000 + (x << 6) + y	Check arena map at x, y and set flag for next UDP
# 10000000 + cm		Set current_move to cm
# 20000000		End program
# 100000000 + c		Delay c cycles

import sys
import os
import math
import json

from path.path_generator import HOST_INDEX_TO_POINTS

class AssemblerError(RuntimeError):
    pass

class Compiler:
    DEFAULT_VELOCITY = 10

    def __init__(self):
        self.instructions = {
            'angle': self.set_angle,
            'vel': self.set_velocity,
            'end': self.end,
            #'jump': self.jump, # jump is disabled for now due to difficulty in using it
            'delay': self.delay,
            'go': self.go,
            'goto': self.goto,
            'shoot': self.shoot,
            'shootpos': self.shootpos,
            'hostcheck': self.hostcheck,
            'chkshoot': self.chkshoot,
            'internal_loc': self.set_internal_location,
            'moving_vel': self.set_moving_velocity
        }

        self.moving_vel = Compiler.DEFAULT_VELOCITY

        self.x = 4
        self.y = 4

    def parse(self, command, args):
        int_args = [int(arg) for arg in args]

        return self.instructions[command](*int_args)

    def set_angle(self, angle):
        return [int(angle)]

    def set_velocity(self, velocity):
        return [1500 + int(velocity)]

    def end(self):
        return [20000000]

    def jump(self, inst):
        raise AssemblerError("jump is difficult to use. Don't use it unless you know what you're doing")
        return [10000000 + 4 * int(inst)]

    def delay(self, cycles):
        return [100000000 + int(cycles)]

    def go(self, pixels):
        time = pixels / (self.moving_vel / 10000)
        return self.set_velocity(self.moving_vel) + \
            self.delay(time) + self.set_velocity(0)

    def get_dist_to(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def get_angle_to(self, x, y):
        # y coordinate must be negative due to layout of coordinates on screen
        dy = -(y - self.y)
        dx = x - self.x

        # angle is flipped according to spimbot angle I/O
        angle = -math.atan2(dy, dx)

        return math.degrees(angle)

    def goto(self, x, y):
        # Highly tuned for consistency and accuracy

        angle = self.get_angle_to(x, y)
        dist = self.get_dist_to(x, y)
        cmd_angle = self.set_angle(angle)
        cmd_go = self.go(dist)

        actual_dist = int(dist / (self.moving_vel / 10000)) * \
            (self.moving_vel / 10000)
        actual_angle = math.radians(-int(angle))

        dx = actual_dist * math.cos(actual_angle)
        # Flip dy again due to coordinate system
        dy = -actual_dist * math.sin(actual_angle)

        self.x = self.x + dx
        self.y = self.y + dy

        return cmd_angle + cmd_go

    def shoot(self):
        return [2000]

    def shootpos(self, x, y):
        angle = self.get_angle_to(x, y)
        cmd = self.set_angle(angle) + self.shoot()
        return cmd

    def hostcheck(self, tile_x, tile_y):
        cmd = 3000 + (tile_x << 6) + tile_y
        return [cmd]

    def chkshoot(self, x, y):
        return self.hostcheck(x // 8, y // 8) + self.shootpos(x, y)

    def set_internal_location(self, x, y):
        self.x = x
        self.y = y

        return []

    def set_moving_velocity(self, moving_velocity):
        self.moving_vel = moving_velocity

        return []


class Lexer:
    def __init__(self, compiler=Compiler):
        self.compiler = compiler()

    def convert_respawn_coordinates(self, pixel_x, pixel_y):
        x = pixel_x // 8
        y = pixel_y // 8

        A = x >= 16
        B = y >= 16
        C = (x // 2 >= 16) if A else (x * 2 >= 16)
        D = (y // 2 >= 16) if B else (y * 2 >= 16)

        host_index = (A << 3) + (B << 2) + (C << 1) + (D << 0)

        return host_index

    def dict_to_array(self, d, size=16):
        arr = [0] * size
        for key, val in d.items():
            arr[key] = val

        return arr

    def copy_lines(self, args, lines):
        args = [int(i) for i in args]

        if len(args) < 3 or len(args) % 2 != 1:
            raise AssemblerError(
                "!!copy must have number of times and at least 1 range: "
                "<times> <start> <end> [<start> <end> ...]")

        times = args[0]
        ranges = [args[i:i + 2] for i in range(1, len(args), 2)]

        new_lines = []

        for r in ranges:
            start = r[0] - 1
            end = r[1]

            new_lines.extend(lines[start:end])

        return new_lines * times

    def preprocess(self, lines):
        lines = [i.strip() for i in lines]

        new_lines = []

        for line in lines:
            if not line or line.startswith('#'):
                # Comment or whitespace
                continue

            if line.startswith('!!'):
                # Preprocessor directive

                command, *args = line.split()

                if command == '!!copy':
                    copied_lines = self.copy_lines(args, lines)
                    new_lines.extend(copied_lines)
            else:
                new_lines.append(line)

        return new_lines

    def parse(self, lines):
        lines = self.preprocess(lines)

        words = []
        respawn_pointers = {}

        for line in lines:
            command, *args = line.split()

            if command.startswith('!'):
                # Special lexer command
                if command == '!respawn':
                    if len(args) == 1:
                        host_index = int(args[0])
                    else:
                        x = int(args[0])
                        y = int(args[1])

                        host_index = self.convert_respawn_coordinates(x, y)

                    # New location is center of host
                    real_x, real_y = HOST_INDEX_TO_POINTS[host_index]

                    self.compiler.set_internal_location(real_x, real_y)
                    respawn_pointers[host_index] = 4 * len(words)

            else:
                # Normal compiled command
                words.extend(self.compiler.parse(command, args))

        str_words = [str(i) for i in words]
        output = ' '.join(['.word'] + str_words)

        respawn_pointers_arr = [str(i) for i in self.dict_to_array(respawn_pointers)]
        respawn_pointers_output = ' '.join(['.word'] + respawn_pointers_arr)

        return output, respawn_pointers_output


if __name__ == '__main__':
    USAGE = """\
error: no AML instruction file specified.

usage:

assemble.py <instruction_file>
    Assembles movement: and respawn_pointers: data segments.
    Outputs JSON to stdout.

assemble.py <instruction_file> <output_file>
    Assembles movement: and respawn_pointers: data segments.
    Outputs JSON to output_file.
    """

    try:
        inst_filename = sys.argv[1]
    except IndexError:
        print(USAGE)
        sys.exit(1)

    if not os.path.exists(inst_filename):
        print('No such file', inst_filename)
        sys.exit(1)

    try:
        output_filename = sys.argv[2]
    except IndexError:
        output_file = sys.stdout
    else:
        output_file = open(output_filename, 'w')

    lexer = Lexer()

    with open(inst_filename) as inst_file:
        lines = inst_file.readlines()

    movement_data, respawn_pointers_data = lexer.parse(lines)

    data = {
        'movement': movement_data,
        'respawn_pointers': respawn_pointers_data
    }

    with output_file:
        json.dump(data, output_file, indent=4)
