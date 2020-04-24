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
import math

class Compiler:
    DEFAULT_VELOCITY = 10

    def __init__(self):
        self.instructions = {
            'angle': self.angle,
            'vel': self.velocity,
            'end': self.end,
            'jump': self.jump,
            'delay': self.delay,
            'go': self.go,
            'goto': self.goto,
            'shoot': self.shoot,
            'shootpos': self.shootpos,
            'hostcheck': self.hostcheck,
            'chkshoot': self.chkshoot,
            'custom_reset': self.custom_reset
        }

        self.x = 4
        self.y = 4

    def parse(self, command, args):
        int_args = [int(arg) for arg in args]

        return self.instructions[command](*int_args)

    @staticmethod
    def angle(angle):
        return [int(angle)]

    @staticmethod
    def velocity(velocity=DEFAULT_VELOCITY):
        return [1500 + int(velocity)]

    @staticmethod
    def end():
        return [90000]

    @staticmethod
    def jump(inst):
        return [10000000 + 4 * int(inst)]

    @staticmethod
    def delay(cycles):
        return [100000000 + int(cycles)]

    @staticmethod
    def go(pixels):
        time = pixels / (Compiler.DEFAULT_VELOCITY / 10000)
        return Compiler.velocity(Compiler.DEFAULT_VELOCITY) + \
            Compiler.delay(time) + Compiler.velocity(0)

    def distTo(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def angleTo(self, x, y):
        # y coordinate must be negative due to layout of coordinates on screen
        dy = -(y - self.y)
        dx = x - self.x

        # angle is flipped according to spimbot angle I/O
        angle = -math.atan2(dy, dx)

        return math.degrees(angle)

    def goto(self, x, y):
        angle = self.angleTo(x, y)
        dist = self.distTo(x, y)
        cmd_angle = self.angle(angle)
        cmd_go = self.go(dist)

        actualDist = int(dist / (Compiler.DEFAULT_VELOCITY / 10000)) * \
            (Compiler.DEFAULT_VELOCITY / 10000)
        actualAngle = math.radians(-int(angle))

        dx = actualDist * math.cos(actualAngle)
        # Flip dy again due to coordinate system
        dy = -actualDist * math.sin(actualAngle)

        self.x = self.x + dx
        self.y = self.y + dy

        return cmd_angle + cmd_go

    @staticmethod
    def shoot():
        return [2000]

    def shootpos(self, x, y):
        angle = self.angleTo(x, y)
        cmd = self.angle(angle) + self.shoot()
        return cmd

    @staticmethod
    def hostcheck(tile_x, tile_y):
        cmd = 3000 + (tile_x << 6) + tile_y
        return [cmd]

    def chkshoot(self, x, y):
        return self.hostcheck(x // 8, y // 8) + self.shootpos(x, y)

    def custom_reset(self):
        return []


class Lexer:
    def __init__(self, compiler=Compiler):
        self.compiler = compiler()

    def parse(self, lines):
        words = []

        line_counter = 0
        rewrite_times = {}
        jump_map = {}

        while line_counter < len(lines):
            line = lines[line_counter]
            line = line.strip()

            if not line.startswith('#'):
                # Not a comment

                command, *args = line.split()

                if command.startswith('!'):
                    # Preprocessor directive

                    if command == '!rewrite':
                        times = int(args[1])
                        rewrite_start_at = int(args[0])

                        if line_counter not in rewrite_times:
                            # Haven't started rewriting yet
                            rewrite_times[line_counter] = times
                            # line_counter is -1 for starting at index of line, not line #
                            # line_counter is -1 again for starting just before the next increment
                            line_counter = rewrite_start_at - 2

                        elif rewrite_times[line_counter] == 0:
                            # Finished rewriting
                            del rewrite_times[line_counter]

                        else:
                            # Rewrote once
                            rewrite_times[line_counter] -= 1
                            line_counter = rewrite_start_at - 2

                    elif command == '!jump':
                        # Be careful with jumping when writing in inst.txt.
                        # Think about what the GENERATED instruction does, not
                        # what the pseudoinstruction in inst.txt does

                        dest = int(args[0])
                        dest_line = dest - 1
                        # dest_line is -1 for starting at index of line, not line #
                        dest_inst = jump_map[dest_line]
                        words.extend(self.compiler.jump(dest_inst))

                else:
                    # Normal compiled command
                    jump_map[line_counter] = len(words)
                    words.extend(self.compiler.parse(command, args))

            line_counter += 1

        str_words = [str(i) for i in words]
        output = ['.word'] + str_words
        return ' '.join(output)


if __name__ == '__main__':
    filename = sys.argv[1]

    lexer = Lexer()

    with open(filename) as f:
        lines = f.readlines()

    output = lexer.parse(lines)

    print(output)
