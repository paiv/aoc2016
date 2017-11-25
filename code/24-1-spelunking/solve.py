#!/usr/bin/env python3
import heapq
import itertools


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


def pos_for_value(x, board):
    w, h = len(board[0]), len(board)

    for row in range(0, h):
        for col in range(0, w):
            if board[row][col] == x:
                return (col, row)
    return None


def format_board(pos, board, pois):
    w, h = len(board[0]), len(board)
    res = '\n'.join(''.join('@' if (col,row) == pos else '*' if (col,row) in pois else board[row][col]
        for col in range(0, w))
        for row in range(0, h))
    return res


def valid_moves(pos, board):
    x, y = pos
    w, h = len(board[0]), len(board)
    moves = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
    moves = [(x, y) for x, y in moves if x >= 0 and y >= 0 and x < w and y < h]
    moves = [(x, y) for x, y in moves if board[y][x] == ' ']
    return moves


def dist(a, b):
    return abs(b[0] - a[0]) + abs(b[1] - a[1])


def path_heur(pos, goal, traveled):
    return len(traveled) + dist(pos, goal)


path_cache = dict()

def find_path(start, goal, board):
    cached = path_cache.get((start, goal), None)
    if cached:
        return cached

    fringe = PriorityQueue()
    visited = set()

    fringe.append((start, []), path_heur(start, goal, []))

    while len(fringe) > 0:
        pos, path = fringe.pop()

        if pos == goal:
            path_cache[(start, goal)] = path
            return path

        if pos in visited:
            continue
        visited.add(pos)

        for child_pos in valid_moves(pos, board):
            child_path = path + [child_pos]
            fringe.append((child_pos, child_path), path_heur(child_pos, goal, child_path))

    return []


def parse_board(text):
    return [list(line) for line in text.splitlines()]


def parse_problem(problem):
    board = parse_board(problem)
    start = pos_for_value('0', board)
    pois = []

    for i in range(1, 10):
        pos = pos_for_value(str(i), board)
        if pos:
            pois.append(pos)

    clear = set(list('.0123456789'))
    clear_board = [[' ' if x in clear else x for x in line] for line in board]

    return (start, pois, clear_board)


def animate(problem, path):
    import time

    start, pois, board = parse_problem(problem)

    print('\n' * 30)
    print(format_board(start, board, pois))

    pois = set(pois)

    for p in path:
        time.sleep(0.5)
        print(format_board(p, board, pois))
        if p in pois:
            pois.remove(p)


def solve(problem):
    path_cache.clear()

    start, pois, board = parse_problem(problem)

    def heur(pos, pois, traveled):
        return sum(dist(pos, p) for p in pois)

    def valid_moves(pos, pois, path):
        moves = []
        for poi in pois:
            child_path = find_path(pos, poi, board)
            if child_path:
                visiting = set(child_path)
                child_pois = [p for p in list(pois) if p not in visiting]
                moves.append((poi, tuple(child_pois), path + child_path))
        return moves


    fringe = PriorityQueue()
    visited = set()

    best_path = None

    state = (start, tuple(pois), [])

    fringe.append(state, heur(*state))

    while len(fringe) > 0:
        pos, pois, path = fringe.pop()

        if len(pois) == 0:
            if best_path is None:
                best_path = path
            elif len(path) < len(best_path):
                best_path = path

        state = (pos, pois, len(path))
        if state in visited:
            continue
        visited.add(state)

        for child in valid_moves(pos, pois, path):
            fringe.append(child, heur(*child))

    # print('solved ({}):\n{}\n   {}'.format(len(best_path), problem, best_path))
    # animate(problem, best_path)
    return len(best_path)


def test():
    assert solve('0') == 0
    assert solve('01') == 1
    assert solve('0.1') == 2
    assert solve('021') == 2
    assert solve('0#1\n...') == 4


    problem = """
###########
#0.1.....2#
#.#######.#
#4.......3#
###########
""".strip()

    assert solve(problem) == 14


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
