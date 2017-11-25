#!/usr/bin/env python3


def count_bits(n):
    total = 0
    while (n):
        total += 1
        n &= n - 1
    return total


def tile(seed, pos):
    x, y = pos
    if x < 0 or y < 0:
        return True
    n = x * x + 3 * x + 2 * x * y + y + y * y + seed
    return count_bits(n) % 2 == 1


def format_path(board, path):
    maxx = max(x for x,y in path)
    maxy = max(y for x,y in path)

    path = set(path)
    lines = []

    for row in range(0, maxy + 2):
        line = ['{:2} '.format(row)]

        for col in range(0, maxx + 2):
            c = '.'
            pos = (col, row)
            if pos in path:
                c = 'o'
            elif board(pos):
                c = '#'
            line.append(c)

        lines.append(''.join(line))

    return '\n'.join(lines)


def solve(problem):
    seed, maxlen = map(int, problem.split())
    orig = (1,1)
    total = 0
    path = []

    def board(pos):
        return tile(seed, pos)

    fringe = list()
    visited = set()

    fringe.append((orig, 0))

    while len(fringe) > 0:
        pos, dist = fringe.pop(0)

        if pos in visited:
            continue
        visited.add(pos)

        path.append(pos)
        total += 1

        if dist >= maxlen:
            continue

        x,y = pos
        for pos in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
            if not board(pos):
                fringe.append((pos, dist + 1))

    # print(format_path(board, path))

    return total


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    print(solve(getinput()))
