#!/usr/bin/env python3


def solve(problem):
    elves = int(problem)

    current = 0
    losers = set()

    while True:
        nextto = (current + 1) % elves
        while nextto in losers:
            nextto = (nextto + 1) % elves

        losers.add(nextto)

        if len(losers) + 1 == elves:
            return current + 1

        current = (nextto + 1) % elves
        while current in losers:
            current = (current + 1) % elves


def test():
    assert solve('3') == 3
    assert solve('5') == 3
    assert solve('6') == 5


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
