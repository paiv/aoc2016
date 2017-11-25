#!/usr/bin/env python3
import heapq
import itertools
import re


class PriorityQueue:
    def __init__(self):
        self.pq = []                         # list of entries arranged in a heap
        self.counter = itertools.count()     # unique sequence count

    def __len__(self):
        return len(self.pq)

    def append(self, task, priority=0):
        count = next(self.counter)
        entry = (priority, count, task)
        heapq.heappush(self.pq, entry)

    def pop(self):
        if self.pq:
            priority, count, task = heapq.heappop(self.pq)
            return task
        raise KeyError('pop from an empty priority queue')


def format_board(elevator, board, names):
    def fmt(i, row):
        floor = 'F{}'.format(i+1)
        elev = 'E' if i == elevator else '.'
        elems = ' '.join(names[k] if row[k] else '.  ' for k,x in enumerate(names))
        return '{} {}  {}'.format(floor, elev, elems)

    text = [fmt(i, row) for i,row in enumerate(board)]
    text = '\n'.join(reversed(text))
    return text


def print_board(elevator, board, names):
    text = format_board(elevator, board, names)
    print(text)


def make_state(el, board):
    # return (el, *(x for row in board for x in row))

    def st(row):
        pairs = sum(row[i] and row[i+1] for i in range(0, len(row), 2))
        loneg = sum(row[i] and not row[i+1] for i in range(0, len(row), 2))
        lonem = sum(not row[i] and row[i+1] for i in range(0, len(row), 2))
        return '{}p{}g{}m'.format(pairs, loneg, lonem)

    state = '|'.join(st(row) for row in board)
    return '{}:{}'.format(el, state)


def format_state(state, names):
    return str(state)

    # elevator = state[0]
    # items = state[1:]
    # board = []
    # for offset in range(0, len(items), len(names)):
    #     row = items[offset: offset + len(names)]
    #     board.append(row)
    # return format_board(elevator, board, names)


def parse_board(text):
    rx = re.compile(r' an? ([\w-]+ \w+)')

    def name(x):
        x = x.split()
        return x[0][0:2].capitalize() + x[1][0].upper()

    things = [rx.findall(line) for line in text.splitlines()]
    things = [set(name(x) for x in xs) for xs in things]

    names = list(sorted(x for line in things for x in line))

    things = [tuple((x in xs) for x in names) for xs in things]

    return things, names


def valid_floor(floor):
    gens = False
    chips = False
    for i in range(0, len(floor), 2):
        if floor[i]:
            gens = True
        elif floor[i + 1]:
            chips = True
    return not (chips and gens)


def heur(board, steps):
    return steps * 4 - sum(i * sum(row) for i, row in enumerate(board))


def solve(text):
    board, names = parse_board(text)
    elevator = 0

    fringe = PriorityQueue()
    visited = set()
    steps = 0

    fringe.append((elevator, board, steps), heur(board, steps))

    print_board(elevator, board, names)

    while len(fringe) > 0:
        elevator, board, steps = fringe.pop()

        if sum(board[3]) == len(names):
            return steps

        state = make_state(elevator, board)
        if state in visited:
            continue
        visited.add(state)

        floors = []
        if elevator < 3:
            floors.append(elevator + 1)
        if elevator > 0:
            floors.append(elevator - 1)

        for inc in floors:
            current_floor_items = list(i for i,v in enumerate(board[elevator]) if v)

            for pair in itertools.combinations(current_floor_items, 2):
                items_left = list(board[elevator])
                items_new = list(board[inc])

                items_left[pair[0]] = False
                items_left[pair[1]] = False
                items_new[pair[0]] = True
                items_new[pair[1]] = True

                if not valid_floor(items_left):
                    continue
                if not valid_floor(items_new):
                    continue

                next_board = list(board)
                next_board[elevator] = tuple(items_left)
                next_board[inc] = tuple(items_new)

                fringe.append((inc, next_board, steps + 1), heur(next_board, steps + 1))

            for idx in current_floor_items:
                items_left = list(board[elevator])
                items_new = list(board[inc])

                items_left[idx] = False
                items_new[idx] = True

                if not valid_floor(items_left):
                    continue
                if not valid_floor(items_new):
                    continue

                next_board = list(board)
                next_board[elevator] = tuple(items_left)
                next_board[inc] = tuple(items_new)

                fringe.append((inc, next_board, steps + 1), heur(next_board, steps + 1))

    print('\n\n'.join(format_state(x, names) for x in visited))
    return -1


def test():
    problem = """
The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
The second floor contains a hydrogen generator.
The third floor contains a lithium generator.
The fourth floor contains nothing relevant.
""".strip()

    # print(format_board(0, *parse_board(problem)))

    # assert format_board(0, *parse_board(problem)) == [set(('HyM', 'LiM')), {'HyG'}, {'LiG'}, set()]

    # assert valid_floor([])
    assert valid_floor([])
    # assert valid_floor(['HyM'])
    assert valid_floor([False, True])
    # assert valid_floor(['HyM', 'LiM'])
    assert valid_floor([True, True])
    # assert valid_floor(['HyM', 'HyG'])
    assert valid_floor([False, True, False, True])
    # assert valid_floor(['HyM', 'HyG', 'LiG'])
    assert valid_floor([True, True, True, False])
    # assert not valid_floor(['HyM', 'LiG'])
    assert not valid_floor([False, True, True, False])
    # assert not valid_floor(['HyM', 'HyG', 'LiM'])
    assert not valid_floor([True, True, False, True])

    assert solve(problem) == 11


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
