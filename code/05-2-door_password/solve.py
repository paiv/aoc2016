#!/usr/bin/env python3
import hashlib
import re


def solve(room):
    index = 0
    res = [None] * 8

    for i in range(0,8):
        while (True):
            text = '{}{}'.format(room, index)
            index += 1
            h = hashlib.md5(text.encode('ascii')).hexdigest()
            if h[:5] == '00000':
                pos = h[5]
                if pos >= '0' and pos <= '7':
                    pos = int(pos)
                    if res[pos] is None:
                        res[pos] = h[6]
                        break

    return ''.join(res)


def test():
    assert solve('abc') == '05ace8e3'


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
