#!/usr/bin/env python3


def fill_step(a):
    b = ''.join('0' if x == '1' else '1' for x in reversed(a))
    return '{}0{}'.format(a, b)


def fill_disk(seed, size):
    data = seed
    while len(data) < size:
        data = fill_step(data)
    return data[:size]


def checksum(data):
    x = list(data)
    while len(x) % 2 == 0:
        x = ['1' if x[i] == x[i+1] else '0' for i in range(0, len(x)-1, 2)]
    return ''.join(x)


def solve(problem):
    size, seed = problem.split()
    size = int(size)
    data = fill_disk(seed, size)
    return checksum(data)


def test():
    assert fill_step('1') == '100'
    assert fill_step('0') == '001'
    assert fill_step('11111') == '11111000000'
    assert fill_step('111100001010') == '1111000010100101011110000'

    assert fill_disk('1', 13) == '1000110010011'

    assert checksum('110010110100') == '100'

    assert solve('20 10000') == '01100'


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
