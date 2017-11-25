#!/usr/bin/env python3
import itertools
import re

#                                       x       y     size     used     avail   use%
df_rx = re.compile(r'/dev/grid/node\-x(\d+)\-y(\d+)\s+(\d+)T\s+(\d+)T\s+\d+T\s+\d+\%')

def parse_df(text):
    nodes = df_rx.findall(text)
    return [tuple(int(x) for x in n) for n in nodes]


def viable(a, b):
    if a[3] > 0:
        if a[3] <= b[2] - b[3] and (a[0] != b[0] or a[1] != b[1]):
            return True
    elif b[3] > 0:
        if b[3] <= a[2] - a[3] and (a[0] != b[0] or a[1] != b[1]):
            return True
    return False


def solve(problem):
    nodes = parse_df(problem)
    return sum(viable(a,b) for a,b in itertools.combinations(nodes, 2))


def test():
    assert parse_df('') == []
    assert parse_df('/dev/grid/node-x0-y1 2T 3T 4T 5%') == [(0,1,2,3)]
    assert parse_df('/dev/grid/node-x0-y1 2T 3T 4T 5%\n/dev/grid/node-x10-y20 80T 40T 30T 50%') == [(0,1,2,3), (10,20,80,40)]

    assert viable((0,0,10,0), (1,0,10,10)) == True
    assert viable((0,0,10,2), (1,0,10,2)) == True
    assert viable((0,0,10,10), (1,0,10,0)) == True
    assert viable((0,0,0,0), (1,0,0,0)) == False
    assert viable((0,0,10,0), (1,0,0,0)) == False
    assert viable((0,0,0,0), (1,0,10,0)) == False
    assert viable((0,0,10,0), (1,0,100,100)) == False
    assert viable((0,0,100,100), (1,0,10,0)) == False
    assert viable((0,0,10,2), (0,0,10,2)) == False


    problem = """
/dev/grid/node-x0-y0     91T    0T    91T    0%
/dev/grid/node-x10-y10   10T    9T     1T   90%
""".strip()
    assert solve(problem) == 1

    problem = """
""".strip()
    assert solve(problem) == 0

    problem = """
/dev/grid/node-x0-y0     91T    0T    91T    0%
""".strip()
    assert solve(problem) == 0

    problem = """
/dev/grid/node-x0-y0     91T    0T    91T    0%
/dev/grid/node-x1-y1      1T    1T     0T  100%
/dev/grid/node-x10-y10   10T    9T     1T   90%
""".strip()
    assert solve(problem) == 3


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
