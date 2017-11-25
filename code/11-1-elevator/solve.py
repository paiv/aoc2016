#!/usr/bin/env python3
import itertools
import re


def print_board(elevator, board):
    def fmt(i, row):
        floor = 'F{}'.format(i+1)
        elev = 'E' if i == elevator else '.'
        elems = ' '.join(row)
        return '{} {}  {}'.format(floor, elev, elems)

    text = [fmt(i, row) for i,row in enumerate(board)]
    text = '\n'.join(reversed(text))
    print(text)


def parse_board(text):
    rx = re.compile(r' a ([\w-]+ \w+)')

    def name(x):
        x = x.split()
        return x[0][0:2].capitalize() + x[1][0].upper()

    things = [rx.findall(line) for line in text.splitlines()]
    things = [[name(x) for x in xs] for xs in things]

    return things


def valid_floor(floor):
    chips = [x for x in floor if x[2] == 'M']
    gens = [g for g in floor if g[2] == 'G']

    if len(gens) == 0:
        return True
    for chip in chips:
        if any(g for g in gens if g[:2] == chip[:2]):
            continue
        if any(g for g in gens if g[:2] != chip[:2]):
            return False
    return True


def solve(text):
    board = parse_board(text)

    def format_state(el, board):
        return '{}:{}'.format(el, '|'.join('.'.join(sorted(line)) for line in board))


    fringe = list()
    visited = set()

    fringe.append((0, board, []))

    print_board(0, board)

    while len(fringe) > 0:
        elevator, board, steps = fringe.pop(0)

        if len(board[0]) == 0 and len(board[1]) == 0 and len(board[2]) == 0:
            # for b in steps:
            #     print()
            #     print_board(0, b)

            return len(steps)

        state = format_state(elevator, board)
        if state in visited:
            continue
        visited.add(state)

        floors = []
        if elevator < 3:
            floors.append(elevator + 1)
        if elevator > 0:
            floors.append(elevator - 1)

        for inc in floors:

            for pair in itertools.combinations(board[elevator], 2):
                next_board = [list(x) for x in board]
                from_floor = next_board[elevator]
                to_floor = next_board[inc]

                from_floor.remove(pair[0])
                from_floor.remove(pair[1])
                to_floor.extend(pair)

                if not valid_floor(from_floor):
                    continue
                if not valid_floor(to_floor):
                    continue

                fringe.append((inc, next_board, steps + [next_board]))

            for item in board[elevator]:
                next_board = [list(x) for x in board]
                from_floor = next_board[elevator]
                to_floor = next_board[inc]

                from_floor.remove(item)
                to_floor.append(item)

                if not valid_floor(from_floor):
                    continue
                if not valid_floor(to_floor):
                    continue

                fringe.append((inc, next_board, steps + [next_board]))

    print('\n'.join(visited))
    return -1


def test():
    problem = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
""".strip()

    assert parse_board(problem) == [['HyM', 'LiM'], ['HyG'], ['LiG'], []]

    assert valid_floor([])
    assert valid_floor(['HyM'])
    assert valid_floor(['HyG'])
    assert valid_floor(['HyM', 'LiM'])
    assert valid_floor(['HyG', 'LiG'])
    assert valid_floor(['HyM', 'HyG'])
    assert valid_floor(['HyM', 'HyG', 'LiG'])
    assert not valid_floor(['HyM', 'LiG'])
    assert not valid_floor(['HyM', 'HyG', 'LiM'])

    assert solve(problem) == 11


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()

    print(solve(getinput()))
