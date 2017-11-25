#!/usr/bin/env python3
import re


def solve(problem):
    rx = re.compile(r'[ULDR]')

    res = []
    pos = 5

    for line in problem.splitlines():
        for m in rx.finditer(line):
            move = m.group(0)
            p = pos

            L = ((pos - 1) // 3) * 3 + 1
            R = L + 2

            if move == 'U':
                p = -3
                if pos + p < 1:
                    p = 0
            elif move == 'D':
                p = 3
                if pos + p > 9:
                    p = 0
            elif move == 'L':
                p = -1
                if pos + p < L:
                    p = 0
            elif move == 'R':
                p = 1
                if pos + p > R:
                    p = 0

            pos += p

        res.append(pos)

    return ''.join((str(x) for x in res))


def test():
    assert solve('U') == '2'
    assert solve('D') == '8'
    assert solve('L') == '4'
    assert solve('R') == '6'
    assert solve('UR') == '3'
    assert solve('U\rR') == '23'
    assert solve('LL') == '4'
    assert solve('RR') == '6'
    assert solve('ULL') == '1'
    assert solve('D\nUUUUD') == '85'
    assert solve('ULL\nRRDDD') == '19'
    assert solve('ULL\nRRDDD\nLURDL') == '198'
    assert solve('ULL\nRRDDD\nLURDL\nUUUUD') == '1985'


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f)


if __name__ == '__main__':
    print(solve(getinput()))
    # test()
