#!/usr/bin/env python3
import re


def checksum(text):
    stats = dict()

    for c in text:
        if c != '-':
            n = stats.get(c, 0)
            stats[c] = n + 1

    index = dict()

    for k,v in stats.items():
        n = index.get(v, [])
        n.append(k)
        n.sort()
        index[v] = n

    chk = sorted(((k,v) for k,v in index.items()), key=lambda x: -x[0])
    chk = (v for k,v in chk)
    chk = ''.join(''.join(x) for x in chk)[:5]

    return chk


room_rx = re.compile(r'([a-z-]+)(\d+)\[([a-z]+)\]')

def get_sectorid(room):
    m = room_rx.match(room)
    if checksum(m.group(1)) == m.group(3):
        return int(m.group(2))


def decipher(name, n):
    def r(c):
        if c == '-':
            return ' '
        c = chr((ord(c) - ord('a') + n) % 26 + ord('a'))
        return c

    return ''.join(r(c) for c in name).strip()


def decrypt(room):
    m = room_rx.match(room)
    name = m.group(1)
    if checksum(name) == m.group(3):
        sectorid = int(m.group(2))
        name = decipher(name, sectorid)
        # print(room, '|', name, sectorid)
        return name, sectorid


def solve(problem, lookfor):
    rooms = (decrypt(room) for room in problem.splitlines())
    rooms = filter(None, rooms)
    res = (v for k,v in rooms if k == lookfor)
    return next(res)


def test():
    assert checksum('aaaaa-bbb-z-y-x') == 'abxyz'
    assert checksum('a-b-c-d-e-f-g-h') == 'abcde'
    assert checksum('not-a-real-room') == 'oarel'

    assert get_sectorid('abc-1[abc]') == 1
    assert get_sectorid('abc-1[x]') == None

    assert decrypt('zab-1[abz]') == ('abc', 1)
    assert decrypt('abc-1[x]') == None

    problem ="""
aaaaa-bbb-z-y-x-123[abxyz]
a-b-c-d-e-f-g-h-987[abcde]
not-a-real-room-404[oarel]
totally-real-room-200[decoy]
mkl-42[klm]
""".strip()

    assert solve(problem, 'cab') == 42


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput(), 'northpole object storage'))
