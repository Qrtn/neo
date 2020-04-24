#!/usr/bin/python3

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

import replace_line

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
            'internal_vel': self.set_internal_velocity
        }

        self.velocity = Compiler.DEFAULT_VELOCITY

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
        raise DeprecationWarning
        return [10000000 + 4 * int(inst)]

    def delay(self, cycles):
        return [100000000 + int(cycles)]

    def go(self, pixels):
        time = pixels / (self.velocity / 10000)
        return self.set_velocity(self.velocity) + \
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

        actual_dist = int(dist / (self.velocity / 10000)) * \
            (self.velocity / 10000)
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

    def set_internal_velocity(self, internal_velocity):
        self.velocity = internal_velocity

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

    def preprocess(self, lines):
        new_lines = []

        for line in lines:
            if line.startswith('!!'):
                # Preprocessor directive

                command, *args = line.split()

                if command == '!!copy':
                    start = int(args[0])
                    end = int(args[1])
                    try:
                        times = int(args[2])
                    except ValueError:
                        times = 1

                    start_index = start - 1
                    end_index = end

                    new_lines.extend(lines[start_index:end_index] * times)
            else:
                new_lines.append(line)

        return new_lines

    def parse(self, lines):
        lines = self.preprocess(lines)

        words = []
        respawn_pointers = {}

        for line in lines:
            line = line.strip()

            if not line or line.startswith('#'):
                # Comment or whitespace
                continue

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
    inst_filename = sys.argv[1]
    try:
        replace = sys.argv[2] == '-r'
    except IndexError:
        replace = False

    if replace:
        asm_filename = sys.argv[3]

        if not os.path.exists(asm_filename):
            print('No such file', asm_filename)
            sys.exit(1)

    lexer = Lexer()

    with open(inst_filename) as f:
        lines = f.readlines()

    output, respawn_pointers_output = lexer.parse(lines)

    print(output)
    print(respawn_pointers_output)

    if replace:
        replace_line.replace_in_file(asm_filename, 'movement:', output + '\n')
        replace_line.replace_in_file(asm_filename, 'respawn_pointers:',
            respawn_pointers_output + '\n')
