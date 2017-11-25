#!/usr/bin/env python3
import re


def solve(problem):

    rx = re.compile(r'(R|L)(\d+)')

    coord = [0,0]
    heading = 1
    visited = set()

    visited.add(tuple(coord))

    for m in rx.finditer(problem):
        turn = m.group(1)
        distance  = int(m.group(2))

        heading = (heading + (1 if turn == 'L' else -1)) % 4

        step = 1 if heading < 2 else -1

        for i in range(0, distance):
            coord[heading % 2] += step

            t = tuple(coord)
            if t in visited:
                return abs(coord[0]) + abs(coord[1])
            else:
                visited.add(t)


def test():
    assert solve('R8, R4, R4, R8') == 4


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f)


if __name__ == '__main__':
    print(solve(getinput()))
    # test()
