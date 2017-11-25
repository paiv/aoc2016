#!/usr/bin/env python3
import re


marker_rx = re.compile(r'\((\d+)x(\d+)\)')

def decompress(text):
    res = []
    i = 0
    while i < len(text):
        if text[i] == '(':
            m = marker_rx.match(text, i)
            dist = int(m.group(1))
            rep = int(m.group(2))
            i = m.end()
            sub = text[i:i+dist]
            res.append(sub * rep)
            i += dist
        else:
            res.append(text[i])
            i += 1

    return ''.join(res)


def solve(text):
    total = 0
    for line in text.splitlines():
        m = decompress(line)
        total += len(m)
    return total


def test():
    assert decompress('ADVENT') == 'ADVENT'
    assert decompress('A(1x5)BC') == 'ABBBBBC'
    assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
    assert decompress('A(2x2)BCD(2x2)EFG') == 'ABCBCDEFEFG'
    assert decompress('(6x1)(1x3)A') == '(1x3)A'
    assert decompress('X(8x2)(3x3)ABCY') == 'X(3x3)ABC(3x3)ABCY'

    problem = """
ADVENT
A(1x5)BC
(3x3)XYZ
A(2x2)BCD(2x2)EFG
(6x1)(1x3)A
X(8x2)(3x3)ABCY
""".strip()

    assert solve(problem) == 57


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
