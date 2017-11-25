#!/usr/bin/env python3
import re


def solve(problem):
    keypad = """
.......
.  1  .
. 234 .
.56789.
. ABC .
.  D  .
.......
"""

    keypad = [list(x) for x in keypad.strip().splitlines()]

    board = dict()

    for row in range(0, len(keypad)):
        line = keypad[row]
        for col in range(0, len(line)):

            def ll(x,y):
                c = keypad[row + y][col + x]
                return c if c > '.' else None

            c = line[col]
            if c > '.':
                board[c] = [ll(1, 0), ll(0, -1), ll(-1, 0), ll(0, 1)]

    # print(board)


    rx = re.compile(r'[ULDR]')

    res = []
    pos = '5'

    for line in problem.splitlines():

        for m in rx.finditer(line):
            move = m.group(0)
            p = pos

            if move == 'U':
                p = board[p][1]
            elif move == 'D':
                p = board[p][3]
            elif move == 'L':
                p = board[p][2]
            elif move == 'R':
                p = board[p][0]

            if p is not None:
                pos = p

        res.append(pos)

    return ''.join((str(x) for x in res))


def test():
    assert solve('U') == '5'
    assert solve('R') == '6'
    assert solve('RR') == '7'
    assert solve('RRU') == '3'
    assert solve('RRL') == '6'
    assert solve('RRD') == 'B'
    assert solve('RRR') == '8'
    assert solve('RRR') == '8'
    assert solve('ULL\nRRDDD\nLURDL\nUUUUD') == '5DB3'


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f)


if __name__ == '__main__':
    print(solve(getinput()))
    # test()
