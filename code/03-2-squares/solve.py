#!/usr/bin/env python3
import re


def solve(problem):
    rx = re.compile(r'\d+')
    total = 0

    def intline(line):
        return [int(x) for x in rx.findall(line)]

    data = [intline(x) for x in problem.splitlines()]
    size = (len(data), len(data[0]))

    rotated = [[0] * size[0] for x in range(0, size[1])]
    for row in range(0, size[0]):
        for col in range(0, size[1]):
            rotated[col][row] = data[row][col]

    data = rotated

    for line in data:
        for i in range(0, len(line), 3):
            sides = line[i:i+3]

            if (sides[0] + sides[1] > sides[2] and
                sides[1] + sides[2] > sides[0] and
                sides[2] + sides[0] > sides[1]):
                total += 1

    return total


def test():
    assert solve('1 3\n1 4\n1 5') == 2



def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    print(solve(getinput()))
    # test()
