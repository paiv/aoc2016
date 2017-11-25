#!/usr/bin/env python3
import itertools
import re


instr_rx = re.compile(r'\s*(add|cpy|inc|dec|jnz|mul|nop|out)\s*(?:([a-d])|(\-?\d+))?\s*(?:([a-d])|(\-?\d+))?')

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


def dump_state(prog, ip, state):
    prog = '\n'.join('{:2}:  {}'.format(i, ' '.join(str(x) for x in p)) for i,p in enumerate(prog))
    state = ' '.join('{}:{}'.format(k, v) for k,v in state.items())
    return 'ip:{} {}\n{}'.format(ip, state, prog)


def vm(prog, state):
    ip = 0
    last_state = (ip, state['a'], state['b'], state['c'], state['d'])
    prog = list(prog)
    instr_count = 0

    # print('-- ', instr_count)
    # print(dump_state(prog, ip, state))

    while ip >= 0 and ip < len(prog):
        instr,x,y = prog[ip]

        instr_count += 1

        if instr == 'nop':
            pass

        elif instr == 'cpy':
            if isinstance(x, str):
                x = state[x]
            state[y] = x

        elif instr == 'inc':
            v = state[x]
            v += 1
            state[x] = v

        elif instr == 'dec':
            v = state[x]
            v -= 1
            state[x] = v

        elif instr == 'jnz':
            if isinstance(x, str):
                x = state[x]
            if x != 0:
                if isinstance(y, str):
                    y = state[y]
                ip += y - 1

        elif instr == 'mul':
            if isinstance(x, str):
                x = state[x]
            state['a'] *= x

        elif instr == 'add':
            if isinstance(x, str):
                x = state[x]
            state['a'] += x

        elif instr == 'out':
            if isinstance(x, str):
                x = state[x]
            yield x

        else:
            raise Exception('invalid instruction {}: {}'.format(ip, prog[ip]))

        ip += 1


        current_state = (ip, state['a'], state['b'], state['c'], state['d'])
        if current_state == last_state:
            print('! killed')
            break
        else:
            last_state = current_state

    # return state


def solve(problem):
    prog = [parse_instr(s) for s in problem.splitlines()]

    for a in range(0,10000000):
        state = make_state()
        state['a'] = a

        g = vm(prog, state)
        out = list(itertools.islice(g, 100))
        print(out)

        if out == [0, 1] * 50:
            return a


def test():
    assert parse_instr('cpy 41 a') == ('cpy', 41, 'a')
    assert parse_instr('cpy -10 c') == ('cpy', -10, 'c')
    assert parse_instr('cpy a b') == ('cpy', 'a', 'b')
    assert parse_instr('inc a') == ('inc', 'a', None)
    assert parse_instr('dec a') == ('dec', 'a', None)
    assert parse_instr('jnz d 2') == ('jnz', 'd', 2)
    assert parse_instr('jnz 0 -2') == ('jnz', 0, -2)
    assert parse_instr('mul b') == ('mul', 'b', None)
    assert parse_instr('mul 2') == ('mul', 2, None)
    assert parse_instr('nop') == ('nop', None, None)
    assert parse_instr('out 2') == ('out', 2, None)
    assert parse_instr('out c') == ('out', 'c', None)

    problem = """
cpy a d
cpy 0 a
out a
cpy 1 a
out a
jnz d -4
""".strip()

    assert solve(problem) == 1


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
