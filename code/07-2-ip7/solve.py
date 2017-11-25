#!/usr/bin/env python3
import re


addr_rx = re.compile(r'\[(\w+)\]|(\b\w+\b)')

def isssl(addr):
    parts = addr_rx.findall(addr)
    hyp = [x for x,y in parts if x]
    sup = [y for x,y in parts if y]

    for s in sup:
        for i in range(0, len(s) - 2):
            aba = s[i: i + 3]
            if aba[0] == aba[2] and aba[0] != aba[1]:
                bab = aba[1] + aba[0] + aba[1]
                for h in hyp:
                    for k in range(0, len(h) - 2):
                        if h[k: k + 3] == bab:
                            return True
    return False


def solve(text):
    return sum(isssl(sig) for sig in text.splitlines())


def test():
    assert isssl('aba[bab]xyz')
    assert not isssl('xyx[xyx]xyx')
    assert isssl('aaa[kek]eke')
    assert isssl('zazbz[bzb]cdb')

    problem = """
aba[bab]xyz
xyx[xyx]xyx
aaa[kek]eke
zazbz[bzb]cdb
""".strip()

    assert solve(problem) == 3


def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()
    print(solve(getinput()))
