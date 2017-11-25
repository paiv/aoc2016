#!/usr/bin/env python3
import copy
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


#                                       x       y     size     used     avail   use%
df_rx = re.compile(r'/dev/grid/node\-x(\d+)\-y(\d+)\s+(\d+)T\s+(\d+)T\s+\d+T\s+\d+\%')

def parse_df(text):
    nodes = df_rx.findall(text)
    return [tuple(int(x) for x in n) for n in nodes]


def make_grid(nodes):
    maxx = max(node[0] for node in nodes)
    maxy = max(node[1] for node in nodes)
    width = maxx + 1
    height = maxy + 1

    size_grid = [[0] * width for i in range(0, height)]
    use_grid = [[0] * width for i in range(0, height)]

    for x,y,p,q in nodes:
        size_grid[y][x] = p
        use_grid[y][x] = q

    return (size_grid, use_grid)


def parse_grid(text):
    nodes = parse_df(text)
    return make_grid(nodes)


def viable(a, b, current_pos, node_size, node_use):
    ax,ay = a
    bx,by = b
    a_use = node_use[ay][ax]

    if a_use > 0 and a != b and (abs(bx - ax) + abs(by - ay)) == 1:
        b_use = node_use[by][bx]
        b_size = node_size[by][bx]

        if a == current_pos:
            if b_use == 0 and a_use <= b_size:
                return True
        elif a_use <= b_size - b_use:
            return True

    return False


def encode_state(a, b):
    # return (pos, tuple(node for row in use_grid for node in row))
    # return tuple(node for row in use_grid for node in row)
    return (a, b)


def heur(data, zero):
    return data[0] + data[1] + abs(data[0] - 1 - zero[0]) + abs(data[1] - zero[1])


def adjacent(pos, grid_size):
    posx,posy = pos
    w,h = grid_size

    res = [(posx, posy - 1), (posx - 1, posy), (posx + 1, posy), (posx, posy + 1)]
    res = [(x,y) for x,y in res if x >= 0 and y >= 0 and x < w and y < h]

    return res


def valid_moves(data, zero, node_size, node_use):
    grid_size = (len(node_size[0]), len(node_size))
    return [m for m in adjacent(zero, grid_size) if viable(m, zero, data, node_size, node_use)]


def children(data, zero, node_size, node_use, steps, path):
    res = []
    for move_from in valid_moves(data, zero, node_size, node_use):

        child_data = zero if move_from == data else data
        child_zero = move_from

        use = copy.deepcopy(node_use)
        use[zero[1]][zero[0]] += use[move_from[1]][move_from[0]]
        use[child_zero[1]][child_zero[0]] = 0

        res.append((child_data, child_zero, use, steps + 1, path + [move_from]))

    return res


def format_grid(grid, data):
    maxx = len(grid[0])
    maxy = len(grid)
    return '\n'.join(''.join('{:>3}'.format('@' if (x,y) == data else '' if grid[y][x] == 0 else grid[y][x]) for x in range(0, maxx)) for y in range(0, maxy))


def format_state(pos, use, steps):
    board = format_grid(use, pos)
    return '{}:\n{}'.format(steps, board)


def pos_of_value(v, grid):
    w = len(grid[0])
    h = len(grid)

    for row in range(0, h):
        for col in range(0, w):
            if grid[row][col] == v:
                return (col, row)

    return None


def animate(node_use, path):
    import time

    data = (len(node_use[0]) - 1, 0)
    zerox,zeroy = pos_of_value(0, node_use)
    state = copy.deepcopy(node_use)

    print('\n' * 40)
    print(format_grid(state, data))

    for x,y in path:
        time.sleep(0.5)

        state[zeroy][zerox] = state[y][x]
        state[y][x] = 0

        if (x,y) == data:
            data = (zerox, zeroy)

        zerox, zeroy = x, y

        print()
        print(format_grid(state, data))


def solve(problem):
    node_size,node_use = parse_grid(problem)
    grid_width = len(node_size[0])
    grid_height = len(node_size)

    fringe = PriorityQueue()
    visited = set()

    goal = (0, 0)
    data = (grid_width - 1, 0)
    zero = pos_of_value(0, node_use)

    fringe.append((data, zero, node_use, 0, []), heur(data, zero))

    while len(fringe) > 0:
        data, zero, use, steps, path = fringe.pop()

        if data == goal:
            print(format_state(data, use, steps))
            print(path)
            print('---')

            animate(node_use, path)

            return steps

        state = encode_state(data, zero)
        if state in visited:
            continue
        visited.add(state)

        for child in children(data, zero, node_size, use, steps, path):
            fringe.append(child, heur(child[0], child[1]))

    print('! not solved')
    print(visited)
    return -1


def test():
    assert parse_df('') == []
    assert parse_df('/dev/grid/node-x0-y1 2T 3T 4T 5%') == [(0,1,2,3)]
    assert parse_df('/dev/grid/node-x0-y1 2T 3T 4T 5%\n/dev/grid/node-x10-y20 80T 40T 30T 50%') == [(0,1,2,3), (10,20,80,40)]

    assert adjacent((1,1), (10, 10)) == [(1,0), (0,1), (2,1), (1,2)]

    problem = """
Filesystem            Size  Used  Avail  Use%
/dev/grid/node-x0-y0   10T    8T     2T   80%
/dev/grid/node-x0-y1   11T    6T     5T   54%
/dev/grid/node-x0-y2   32T   28T     4T   87%
/dev/grid/node-x1-y0    9T    7T     2T   77%
/dev/grid/node-x1-y1    8T    0T     8T    0%
/dev/grid/node-x1-y2   11T    7T     4T   63%
/dev/grid/node-x2-y0   10T    6T     4T   60%
/dev/grid/node-x2-y1    9T    8T     1T   88%
/dev/grid/node-x2-y2    9T    6T     3T   66%
""".strip()

    assert solve(problem) == 7


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
