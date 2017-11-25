#!/usr/bin/env python3


def solve(problem):
    lines = problem.splitlines()
    lines = sorted(tuple(int(k) for k in x.split('-')) for x in lines)

    x = 0
    m = -1
    for a,b in lines:
        if x < a:
            return x
        m = max(m, b)
        x = m + 1


def test():
    problem = """
5-8
0-2
4-7
""".strip()

    assert solve(problem) == 3


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
