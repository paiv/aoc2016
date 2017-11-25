#!/usr/bin/env python3


traps = set(['..^', '.^^', '^..', '^^.'])

def safe(text):
    return text not in traps

def getrow(uprow):
    line = '.{}.'.format(uprow)
    res = ''.join('.' if safe(line[i:i+3]) else '^' for i in range(0, len(line) - 2))
    return res


def solve(problem, rows=400000):
    row = problem

    def nsafe(line):
        return sum(c == '.' for c in line)

    total = nsafe(row)

    for i in range(1, rows):
        row = getrow(row)
        total += nsafe(row)

    return total


def test():
    assert safe('...') # 0
    assert safe('.^.') # 2
    assert safe('^.^') # 5
    assert safe('^^^') # 7
    assert not safe('..^') # 1
    assert not safe('.^^') # 3
    assert not safe('^..') # 4
    assert not safe('^^.') # 6

    assert getrow('...') == '...'
    assert getrow('^..') == '.^.'
    assert getrow('.^.') == '^.^'
    assert getrow('..^') == '.^.'
    assert getrow('^^.') == '^^^'
    assert getrow('.^^') == '^^^'

    assert solve('..^^.', 3) == 6
    assert solve('.^^.^.^^^^', 10) == 38


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
