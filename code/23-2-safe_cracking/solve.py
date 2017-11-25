#!/usr/bin/env python3
import re


instr_rx = re.compile(r'\s*(cpy|inc|dec|jnz|tgl|mul|nop)\s*(?:([a-d])|(\-?\d+))?\s*(?:([a-d])|(\-?\d+))?')

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


def toggle_instr(instr):
    instr,x,y = instr

    if instr == 'inc':
        instr = 'dec'
    elif instr in ('dec', 'tgl'):
        instr = 'inc'
    elif instr == 'jnz':
        instr = 'cpy'
    elif instr == 'cpy':
        instr = 'jnz'

    return (instr, x, y)


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

        elif instr == 'tgl':
            if isinstance(x, str):
                x = state[x]
            x += ip
            if x >= 0 and x < len(prog):
                prog[x] = toggle_instr(prog[x])

                # print('-- ', instr_count)
                # print(dump_state(prog, ip, state))

        else:
            raise 'invalid instruction {}: {}'.format(ip, prog[ip])

        ip += 1


        current_state = (ip, state['a'], state['b'], state['c'], state['d'])
        if current_state == last_state:
            print('! killed')
            break
        else:
            last_state = current_state

    return state


def solve(problem, a=0):
    prog = [parse_instr(s) for s in problem.splitlines()]
    state = make_state()

    state['a'] = a

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
    assert parse_instr('tgl a') == ('tgl', 'a', None)
    assert parse_instr('tgl 2') == ('tgl', 2, None)
    assert parse_instr('mul b') == ('mul', 'b', None)
    assert parse_instr('mul 2') == ('mul', 2, None)
    assert parse_instr('nop') == ('nop', None, None)

    assert toggle_instr(('inc', 'a', None)) == ('dec', 'a', None)
    assert toggle_instr(('inc', 2, None)) == ('dec', 2, None)
    assert toggle_instr(('dec', 'a', None)) == ('inc', 'a', None)
    assert toggle_instr(('tgl', 'a', None)) == ('inc', 'a', None)
    assert toggle_instr(('jnz', 'a', 2)) == ('cpy', 'a', 2)
    assert toggle_instr(('cpy', 'a', 2)) == ('jnz', 'a', 2)

    assert solve('cpy 1 a') == 1
    assert solve('inc a') == 1
    assert solve('dec a') == -1
    assert solve('cpy 10 a\ndec a\njnz a -1') == 0
    assert solve('cpy 42 a\ntgl 1\ninc a') == 41
    assert solve('cpy 42 a\ntgl 1\ndec a') == 43
    assert solve('cpy 42 a\ntgl 1\ntgl a') == 43
    assert solve('cpy -1 a\ntgl 1\njnz 1 a') == 1
    assert solve('cpy 42 a\ntgl 1\ncpy 0 a') == 42
    assert solve('nop\nnop\ncpy 42 a') == 42
    assert solve('cpy 3 a\ncpy a b\ninc b\nmul b') == 12


    problem = """
cpy 2 a
tgl a
tgl a
tgl a
cpy 1 a
dec a
dec a
""".strip()

    assert solve(problem) == 3


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput(), a=12))
