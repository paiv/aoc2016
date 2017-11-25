#!/usr/bin/env python3
import hashlib
import re


def solve(noise):
    noise = noise.splitlines()
    w = len(noise[0])
    res = []

    for i in range(0, w):
        stats = dict()
        for line in noise:
            c = line[i]
            n = stats.get(c, 0)
            stats[c] = n + 1

        stats = sorted(((k,v) for k,v in stats.items()), key=lambda x: -x[1])
        top = stats[0]
        res.append(top[0])

    return ''.join(res)


def test():
    problem = """
eedadn
drvtee
eandsr
raavrd
atevrs
tsrnev
sdttsa
rasrtv
nssdts
ntnada
svetve
tesnvt
vntsnd
vrdear
dvrsen
enarar
""".strip()

    assert solve(problem) == 'easter'


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
