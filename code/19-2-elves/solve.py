#!/usr/bin/env python3
import math


def solve0(problem):
    elves = int(problem)

    names = [i for i in range(1, elves+1)]
    current = 0

    while True:
        nextto = (current + len(names) // 2) % len(names)

        names.pop(nextto)

        if len(names) == 1:
            return names[0]

        if current > nextto:
            current = current % len(names)
        else:
            current = (current + 1) % len(names)


def dump_data():
    res = ((i, solve0(str(i))) for i in range(2, 2210))
    res = '\n'.join(', '.join((str(i), str(x))) for i,x in res)
    print('n, x')
    print(res)


def solve(problem):
    elves = int(problem)

    t = int(math.log(elves, 3))
    r = 3**t
    R = 3**(t+1)
    m = R - r

    if elves == r:
        return r
    elif elves <= m:
        return elves - r
    else:
        return elves * 2 - R


def test():
    assert solve('2') == 1
    assert solve('3') == 3
    assert solve('4') == 1
    assert solve('5') == 2
    assert solve('6') == 3
    assert solve('7') == 5
    assert solve('10') == 1

    assert solve('65535') == 6486
    assert solve('65536') == 6487
    assert solve('65537') == 6488


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
