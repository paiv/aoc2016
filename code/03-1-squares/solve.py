#!/usr/bin/env python3
import re


def solve(problem):
    rx = re.compile(r'\d+')
    total = 0

    def intline(line):
        return [int(x) for x in rx.findall(line)]

    data = [intline(x) for x in problem.splitlines()]

    for sides in data:

        if (sides[0] + sides[1] > sides[2] and
            sides[1] + sides[2] > sides[0] and
            sides[2] + sides[0] > sides[1]):
            total += 1

    return total


def test():
    assert solve('1 1 1') == 1
    assert solve('1 1 2') == 0
    assert solve('3 4 5') == 1
    assert solve('1 1 2\n3 4 5') == 1



def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    print(solve(getinput()))
    # test()
