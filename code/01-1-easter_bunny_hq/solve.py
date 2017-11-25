#!/usr/bin/env python3
import re


def solve(problem):

    rx = re.compile(r'(R|L)(\d+)')

    coord = [0,0]
    heading = 1

    for m in rx.finditer(problem):
        turn = m.group(1)
        distance  = int(m.group(2))

        heading = (heading + (1 if turn == 'L' else -1)) % 4

        if heading > 1:
            distance = -distance

        coord[heading % 2] += distance

    return abs(coord[0]) + abs(coord[1])


def test():
    assert solve('R2, L3') == 5
    assert solve('R2, R2, R2') == 2
    assert solve('R5, L5, R5, R3') == 12
    assert solve('R1, R1') == 2


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f)


if __name__ == '__main__':
    print(solve(getinput()))
    # test()
