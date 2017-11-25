#!/usr/bin/env python3
import hashlib


def room_locks(seed, path):
    m = seed + path
    h = hashlib.md5(m.encode('ascii')).hexdigest()[:4]
    return tuple(x > 'a' for x in h)


def check_pos(x, y, i):
    if i == 0: # up
        return y > 0
    elif i == 1: # down
        return y < 3
    elif i == 2: # left
        return x > 0
    elif i == 3: # right
        return x < 3
    else:
        return False


def move_pos(x, y, i, path):
    if i == 0: # up
        return ((x, y - 1), path + 'U')
    elif i == 1: # down
        return ((x, y + 1), path + 'D')
    elif i == 2: # left
        return ((x - 1, y), path + 'L')
    elif i == 3: # right
        return ((x + 1, y), path + 'R')
    else:
        return ((x, y), path)


def get_valid(pos, seed, path):
    l = room_locks(seed, path)
    valid = [move_pos(*pos, i, path) for i,x in enumerate(l) if x and check_pos(*pos, i)]
    return valid


def render_path(orig, path):
    x, y = orig
    res = [orig]
    for mov in path:
        if mov == 'U':
            y -= 1
        elif mov == 'D':
            y += 1
        elif mov == 'L':
            x -= 1
        elif mov == 'R':
            x += 1
        res.append((x, y))
    return res


def solve(problem):
    seed = problem
    orig = (0, 0)
    goal = (3, 3)

    fringe = list()
    fringe.append((orig, ''))

    best_path = ''

    while len(fringe) > 0:
        pos, path = fringe.pop(0)

        if pos == goal:
            if len(path) > len(best_path):
                best_path = path
            continue

        for child in get_valid(pos, seed, path):
            fringe.append(child)

    # print(len(best_path), best_path)
    # print(render_path(orig, best_path))

    return len(best_path)


def test():
    #                                   up   down  left  right
    assert room_locks('hijkl', '') == (True, True, True, False)
    assert room_locks('hijkl', 'D') == (True, False, True, True)
    assert room_locks('hijkl', 'DR') == (False, False, False, False)
    assert room_locks('hijkl', 'DU') == (False, False, False, True)
    assert room_locks('hijkl', 'DUR') == (False, False, False, False)

    assert get_valid((0,0), 'hijkl', '') == [((0,1), 'D')]
    assert get_valid((0,1), 'hijkl', 'D') == [((0,0), 'DU'), ((1,1), 'DR')]

    assert solve('ihgpwlah') == 370
    assert solve('kglvqrro') == 492
    assert solve('ulqzkmiv') == 830


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
