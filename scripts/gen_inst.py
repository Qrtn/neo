#!/usr/bin/python3

### Movement Pattern
# -360 to 360	absolute angle
# 1500 +- v	velocity
# 2000		UDP, may be contingent on previous check of arena map
# 3000 + x	Check arena map, x
# 3000 + y	Check arena map, y
# 90000		End program
# 100000 + cm	Set current_move to cm
# 100000000 + c	Delay c cycles

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
            'goto': self.goto
        }

        self.x = 0
        self.y = 0

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
        return [100000 + 4 * (int(inst) - 1)]

    @staticmethod
    def delay(cycles):
        return [100000000 + int(cycles)]

    @staticmethod
    def go(pixels):
        time = pixels / (Compiler.DEFAULT_VELOCITY / 100000)
        return Compiler.velocity(Compiler.DEFAULT_VELOCITY) + \
            Compiler.delay(time) + Compiler.velocity(0)

    def distTo(self, x, y):
        return math.sqrt((x - self.x) ** 2 + (y - self.y) ** 2)

    def angleTo(self, x, y):
        return math.atan2(y - self.y, x - self.x)

    def goto(self, x, y):
        cmd = self.angle(self.angleTo(x, y)) + self.go(self.distTo(x, y))
        self.x = x
        self.y = y
        return cmd


class Lexer:
    def __init__(self, compiler=Compiler):
        self.compiler = compiler()

    def parse(self, stream):
        words = []

        for line in stream:
            command, *args = line.split()
            words.extend(self.compiler.parse(command, args))

        output = ['.word'] + [str(i) for i in words]
        return ' '.join(output)


if __name__ == '__main__':
    filename = sys.argv[1]

    lexer = Lexer()

    with open(filename) as f:
        output = lexer.parse(f)

    print(output)
