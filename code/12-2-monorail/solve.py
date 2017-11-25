#!/usr/bin/env python3
import re


instr_rx = re.compile(r'\s*(cpy|inc|dec|jnz)\s+(?:([a-d])|(\-?\d+))\s*(?:([a-d])|(\-?\d+))?')

def parse_instr(text):
    m = instr_rx.match(text)

    instr = m.group(1)
    x = None
    y = None

    if m.group(2):
        x = m.group(2)
    elif m.group(3):
        x = int(m.group(3))

    if m.group(4):
        y = m.group(4)
    elif m.group(5):
        y = int(m.group(5))

    return (instr, x, y)


def make_state(a=0, b=0, c=0, d=0):
    return {
        'a': a,
        'b': b,
        'c': c,
        'd': d,
    }


def vm(prog, state):
    ip = 0
    last_state = (ip, state['a'], state['b'], state['c'], state['d'])

    while ip >= 0 and ip < len(prog):
        instr,x,y = prog[ip]

        if instr == 'cpy':
            if isinstance(x, str):
                x = state[x]
            state[y] = x
            ip += 1
        elif instr == 'inc':
            v = state[x]
            v += 1
            state[x] = v
            ip += 1
        elif instr == 'dec':
            v = state[x]
            v -= 1
            state[x] = v
            ip += 1
        elif instr == 'jnz':
            if isinstance(x, str):
                x = state[x]
            if x != 0:
                ip += y
            else:
                ip += 1

        current_state = (ip, state['a'], state['b'], state['c'], state['d'])
        if current_state == last_state:
            print('! killed')
            break
        else:
            last_state = current_state

    return state


def solve(problem):
    prog = [parse_instr(s) for s in problem.splitlines()]
    state = make_state(c=1)
    vm(prog, state)
    return state['a']


def test():
    assert parse_instr('cpy 41 a') == ('cpy', 41, 'a')
    assert parse_instr('cpy -10 c') == ('cpy', -10, 'c')
    assert parse_instr('cpy a b') == ('cpy', 'a', 'b')
    assert parse_instr('inc a') == ('inc', 'a', None)
    assert parse_instr('dec a') == ('dec', 'a', None)
    assert parse_instr('jnz d 2') == ('jnz', 'd', 2)
    assert parse_instr('jnz 0 -2') == ('jnz', 0, -2)

    assert solve('cpy 1 a') == 1
    assert solve('inc a') == 1
    assert solve('dec a') == -1
    assert solve('cpy 10 a\ndec a\njnz a -1') == 0


    problem = """
cpy 41 a
inc a
inc a
dec a
jnz a 2
dec a
""".strip()

    assert solve(problem) == 42


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
