#!/usr/bin/env python3
import re


disc_rx = re.compile(r'Disc \#\d+ has (\d+) positions; at time=0, it is at position (\d+)\.')

def parse_disc(text):
    m = disc_rx.match(text)
    p = int(m.group(1))
    x = int(m.group(2))
    return (p, x)


def all_align(discs, t):
    for m,x in discs:
        t += 1
        if (x + t) % m != 0:
            return False
    return True


def solve(problem):
    discs = [parse_disc(x) for x in problem.splitlines()]

    t = 0
    while (True):
        if all_align(discs, t):
            return t
        t += 1


def test():
    assert parse_disc('Disc #1 has 5 positions; at time=0, it is at position 4.') == (5, 4)
    assert parse_disc('Disc #2 has 2 positions; at time=0, it is at position 1.') == (2, 1)

    problem = """
Disc #1 has 5 positions; at time=0, it is at position 4.
Disc #2 has 2 positions; at time=0, it is at position 1.
""".strip()

    assert solve(problem) == 5


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
