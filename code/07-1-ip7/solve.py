#!/usr/bin/env python3
import re


def abba(text):
    for i in range(0, len(text) - 3):
        s = text[i:i+4]
        if s[0] != s[1]:
            if s[0] == s[3] and s[1] == s[2]:
                return True
    return False


addr_rx = re.compile(r'(\[\w+\])|(\b\w+\b)')

def istls(addr):
    res = False
    for m in addr_rx.finditer(addr):
        if m.group(0)[0] == '[':
            if abba(m.group(1)):
                return False
        elif abba(m.group(0)):
            res = True
    return res


def solve(text):
    return sum(istls(sig) for sig in text.splitlines())


def test():
    assert not abba('')
    assert abba('abba')
    assert not abba('aaaa')
    assert abba('axyyxzz')

    assert istls('abba[mnop]qrst')
    assert not istls('abcd[bddb]xyyx')
    assert not istls('aaaa[qwer]tyui')
    assert istls('ioxxoj[asdfgh]zxcvbn')
    assert istls('xyyx[mnop]abba[foob]ar')
    assert not istls('xyyx[mnop]foob[abba]ar')

    problem = """
abba[mnop]qrst
abcd[bddb]xyyx
aaaa[qwer]tyui
ioxxoj[asdfgh]zxcvbn
""".strip()

    assert solve(problem) == 2


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
