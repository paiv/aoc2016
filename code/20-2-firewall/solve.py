#!/usr/bin/env python3


def solve(problem, w=4294967295):
    lines = problem.splitlines()
    lines = sorted(tuple(int(k) for k in x.split('-')) for x in lines)

    x = 0
    m = -1
    total = 0

    for a,b in lines:
        if x < a:
            total += a - x
        m = max(m, b)
        x = m + 1

    if x < w:
        total += w - x
    return total


def test():
    problem = """
5-8
0-2
4-7
""".strip()

    assert solve(problem, 10) == 2


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    test()
    print(solve(getinput()))
