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
    DEFAULT_VELOCITY = 2

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
            'shootpos': self.shootpos
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
        return [100000 + 4 * (int(inst) - 1)]

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
        cmd = self.angle(angle) + self.go(dist)

        actualDist = int(dist)
        actualAngle = math.radians(-int(angle))

        dx = actualDist * math.cos(actualAngle)
        # Flip dy again due to coordinate system
        dy = -actualDist * math.sin(actualAngle)

        self.x = self.x + dx
        self.y = self.y + dy

        return cmd

    @staticmethod
    def shoot():
        return [2000]

    def shootpos(self, x, y):
        angle = self.angleTo(x, y)
        cmd = self.angle(angle) + self.shoot()
        return cmd


class Lexer:
    def __init__(self, compiler=Compiler):
        self.compiler = compiler()

    def parse(self, stream):
        words = []

        for i in range(15):
            for line in stream:
                line = line.strip()

                if line.startswith('#'):
                    continue

                command, *args = line.split()
                words.extend(self.compiler.parse(command, args))

            stream.seek(0)

        words.extend(self.compiler.end())
        str_words = [str(i) for i in words]
        output = ['.word'] + str_words
        return ' '.join(output)


if __name__ == '__main__':
    filename = sys.argv[1]

    lexer = Lexer()

    with open(filename) as f:
        output = lexer.parse(f)

    print(output)
