#!/usr/bin/env python3
import re


marker_rx = re.compile(r'\((\d+)x(\d+)\)')

def decompress(text):
    total = 0
    i = 0
    while i < len(text):
        if text[i] == '(':
            has_markers = True
            m = marker_rx.match(text, i)
            dist = int(m.group(1))
            rep = int(m.group(2))
            i = m.end()
            sub = text[i:i+dist]
            total += decompress(sub) * rep
            i += dist
        else:
            total += 1
            i += 1

    return total


def solve(text):
    total = 0
    for line in text.splitlines():
        m = decompress(line)
        total += m
    return total


def test():
    # assert decompress('(3x3)XYZ') == 'XYZXYZXYZ'
    # assert decompress('X(8x2)(3x3)ABCY') == 'XABCABCABCABCABCABCY'
    # assert decompress('(27x12)(20x12)(13x14)(7x10)(1x12)A') == 'A' * 241920
    # assert len(decompress('(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN')) == 445

    problem = """
(3x3)XYZ
X(8x2)(3x3)ABCY
(27x12)(20x12)(13x14)(7x10)(1x12)A
(25x3)(3x3)ABC(2x3)XY(5x2)PQRSTX(18x9)(3x2)TWO(5x7)SEVEN
""".strip()

    assert solve(problem) == 9 + 20 + 241920 + 445


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
