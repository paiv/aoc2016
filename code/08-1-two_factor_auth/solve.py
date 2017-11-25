#!/usr/bin/env python3
import re
import numpy as np


def rect(shape, screen):
    x,y = shape
    t = np.ones((y,x))
    screen[:y, :x] = t
    return screen


def rotate_col(col, n, screen):
    t = screen[:,col]
    t = np.roll(t, n)
    screen[:,col] = t
    return screen


def rotate_row(row, n, screen):
    t = screen[row,:]
    t = np.roll(t, n)
    screen[row,:] = t
    return screen


def display(screen):
    s = '\n'.join(''.join(['#' if c else '.' for c in row]) for row in screen)
    print(s)


command_rx = re.compile(r'rect (\d+)x(\d+)|rotate column x=(\d+) by (\d+)|rotate row y=(\d+) by (\d+)')

def parse_command(text):
    m = command_rx.match(text)

    if m.group(1):
        return ('rect', int(m.group(1)), int(m.group(2)))
    elif m.group(3):
        return ('rx', int(m.group(3)), int(m.group(4)))
    elif m.group(5):
        return ('ry', int(m.group(5)), int(m.group(6)))


def run_commands(screen, text):
    for line in text.splitlines():
        cmd, a, b = parse_command(line)
        if cmd == 'rect':
            rect((a, b), screen)
        elif cmd == 'rx':
            rotate_col(a, b, screen)
        elif cmd == 'ry':
            rotate_row(a, b, screen)


def solve(text, shape):
    screen = np.zeros((shape[1], shape[0]), dtype=np.int)
    run_commands(screen, text)
    n = np.sum(screen)
    return n


def test():
    screen = np.zeros((3, 7))

    rect((3, 2), screen)
    assert np.all(screen == np.array([[1,1,1,0,0,0,0],[1,1,1,0,0,0,0],[0,0,0,0,0,0,0]]))

    rotate_col(1, 1, screen)
    assert np.all(screen == np.array([[1,0,1,0,0,0,0],[1,1,1,0,0,0,0],[0,1,0,0,0,0,0]]))

    rotate_row(0, 4, screen)
    assert np.all(screen == np.array([[0,0,0,0,1,0,1],[1,1,1,0,0,0,0],[0,1,0,0,0,0,0]]))

    rotate_col(1, 1, screen)
    assert np.all(screen == np.array([[0,1,0,0,1,0,1],[1,0,1,0,0,0,0],[0,1,0,0,0,0,0]]))

    problem = """
rect 3x2
rotate column x=1 by 1
rotate row y=0 by 4
rotate column x=1 by 1
""".strip()

    screen = np.zeros((3, 7))
    run_commands(screen, problem)
    assert np.all(screen == np.array([[0,1,0,0,1,0,1],[1,0,1,0,0,0,0],[0,1,0,0,0,0,0]]))

    assert solve(problem, (7, 3)) == 6


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput(), (50, 6)))
