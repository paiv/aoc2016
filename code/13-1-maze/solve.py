#!/usr/bin/env python3


def count_bits(n):
    total = 0
    while (n):
        total += 1
        n &= n - 1
    return total


def tile(seed, pos):
    x, y = pos
    n = x * x + 3 * x + 2 * x * y + y + y * y + seed
    return count_bits(n) % 2 == 1


def find_path(board, orig, goal):
    fringe = list()
    visited = set()

    fringe.append([orig])

    while len(fringe) > 0:
        current = fringe.pop(0)
        pos = current[-1]

        if pos == goal:
            return current

        if pos in visited:
            continue
        visited.add(pos)

        x,y = pos
        for pos in [(x+1,y), (x-1,y), (x,y+1), (x,y-1)]:
            if not board(pos):
                fringe.append(current + [pos])

    return orig


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
    seed, goalx, goaly = map(int, problem.split())

    def genmap(pos):
        return tile(seed, pos)

    path = find_path(genmap, (1,1), (goalx, goaly))

    print(format_path(genmap, path))

    return len(path) - 1


def test():
    assert count_bits(0) == 0
    assert count_bits(1) == 1
    assert count_bits(2) == 1
    assert count_bits(3) == 2
    assert count_bits(10) == 2
    assert count_bits(15) == 4
    assert count_bits(32) == 1

    assert tile(10, (0, 0)) == False
    assert tile(10, (0, 1)) == False
    assert tile(10, (1, 0)) == True
    assert tile(10, (1, 1)) == False
    assert tile(10, (4, 3)) == True
    assert tile(10, (9, 6)) == True

    assert solve('10 7 4') == 11


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
