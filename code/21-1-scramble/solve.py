#!/usr/bin/env python3
import re


instr_rx = re.compile(r'swap position (\d+) with position (\d+)|swap letter (\w) with letter (\w)|rotate (left|right) (\d+) steps?|rotate based on position of letter (\w)|reverse positions (\d+) through (\d+)|move position (\d+) to position (\d+)')

def parse_instr(text):
    m = instr_rx.match(text)

    instr = None
    x = None
    y = None

    if m.group(1):
        instr = 'swap'
        x = int(m.group(1))
        y = int(m.group(2))
    elif m.group(3):
        instr = 'swal'
        x = m.group(3)
        y = m.group(4)
    elif m.group(5):
        if m.group(5) == 'left':
            instr = 'rotl'
        elif m.group(5) == 'right':
            instr = 'rotr'
        x = int(m.group(6))
    elif m.group(7):
        instr = 'rotp'
        x = m.group(7)
    elif m.group(8):
        instr = 'rev'
        x = int(m.group(8))
        y = int(m.group(9))
    elif m.group(10):
        instr = 'move'
        x = int(m.group(10))
        y = int(m.group(11))

    return (instr, x, y)


def vm(prog, state):
    state = list(state)

    for instr,x,y in prog:

        if instr == 'swap':
            state[x], state[y] = state[y], state[x]
        elif instr == 'swal':
            x = state.index(x)
            y = state.index(y)
            state[x], state[y] = state[y], state[x]
        elif instr == 'rev':
            s = state[x:y+1]
            s.reverse()
            state[x:y+1] = s
        elif instr == 'rotl':
            state = state[x:] + state[:x]
        elif instr == 'rotr':
            state = state[-x:] + state[:-x]
        elif instr == 'rotp':
            x = state.index(x)
            if x >= 4:
                x += 1
            x += 1
            x = x % len(state)
            state = state[-x:] + state[:-x]
        elif instr == 'move':
            s = state.pop(x)
            state.insert(y, s)

    return ''.join(state)


def solve(problem, seed='abcdefgh'):
    prog = [parse_instr(s) for s in problem.splitlines()]
    return vm(prog, seed)


def test():
    assert parse_instr('swap position 4 with position 0') == ('swap', 4, 0)
    assert parse_instr('swap letter d with letter b') == ('swal', 'd', 'b')
    assert parse_instr('rotate left 1 step') == ('rotl', 1, None)
    assert parse_instr('rotate right 3 steps') == ('rotr', 3, None)
    assert parse_instr('rotate based on position of letter b') == ('rotp', 'b', None)
    assert parse_instr('reverse positions 12 through 70') == ('rev', 12, 70)
    assert parse_instr('move position 1 to position 4') == ('move', 1, 4)

    assert solve('swap position 4 with position 0', 'abcde') == 'ebcda'
    assert solve('swap letter d with letter b', 'ebcda') == 'edcba'
    assert solve('reverse positions 0 through 4', 'edcba') == 'abcde'
    assert solve('rotate left 1 step', 'abcde') == 'bcdea'
    assert solve('move position 1 to position 4', 'bcdea') == 'bdeac'
    assert solve('move position 3 to position 0', 'bdeac') == 'abdec'
    assert solve('rotate based on position of letter b', 'abdec') == 'ecabd'
    assert solve('rotate based on position of letter d', 'ecabd') == 'decab'

    assert solve('rotate right 1 step', 'abcde') == 'eabcd'
    assert solve('rotate right 3 steps', 'abcde') == 'cdeab'
    assert solve('rotate left 3 steps', 'abcde') == 'deabc'


    problem = """
swap position 4 with position 0
swap letter d with letter b
reverse positions 0 through 4
rotate left 1 step
move position 1 to position 4
move position 3 to position 0
rotate based on position of letter b
rotate based on position of letter d
""".strip()

    assert solve(problem, 'abcde') == 'decab'


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
