#!/usr/bin/env python3
import hashlib
import re


def solve(room):
    index = 0
    res = []
    for i in range(0,8):
        while (True):
            text = '{}{}'.format(room, index)
            index += 1
            h = hashlib.md5(text.encode('ascii')).hexdigest()
            if h[:5] == '00000':
                res.append(h[5])
                break

    return ''.join(res)


def test():
    assert solve('abc') == '18f47a30'


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
