#!/usr/bin/env python3
import hashlib
import itertools


def keystream(seed):
    i = 0
    while (True):
        m = '{}{}'.format(seed, i)
        for k in range(0, 2017):
            m = hashlib.md5(m.encode('ascii')).hexdigest()
        yield i,m
        i += 1


def search3(key):
    for i in range(0, len(key) - 2):
        c = key[i]
        xx = c * 3
        if key[i:i+3] == xx:
            return c

def search5(i, key, c):
    xx = c[0] * 5
    if xx in key:
        # print('found ', xx, ' in ', i, key)
        return True
    return False


def solve(problem):
    seed = problem
    goal = 64

    total = 0
    last_index = -1

    keys = keystream(seed)

    while total < goal:
        i,key = next(keys)

        match3 = search3(key)
        if match3:
            keys, g1 = itertools.tee(keys)

            valid = False
            for k in range(0, 1000):
                ii,sub = next(g1)
                if search5(ii, sub, match3):
                    valid = True
                    break

            if valid:
                last_index = i
                total += 1

                # print(total, i, key)

    return last_index


def test():
    assert next(keystream('abc')) == (0, 'a107ff634856bb300138cac6568c0f24')
    assert solve('abc') == 22551


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
