#!/usr/bin/env python3
import re


command_rx = re.compile(r'value (\d+) goes to (.*)|bot (\d+) gives low to (\w+\s+\w+) and high to (.*)')
target_rx = re.compile(r'bot (\d+)|output (\d+)')


def parse_target(text):
    m = target_rx.match(text)
    if m.group(1):
        return ('bot', int(m.group(1)))
    elif m.group(2):
        return ('out', int(m.group(2)))


def parse_command(text):
    m = command_rx.match(text)
    if m.group(1):
        return (('val', int(m.group(1))), parse_target(m.group(2)), None)
    elif m.group(3):
        return (('bot', int(m.group(3))), parse_target(m.group(4)), parse_target(m.group(5)))
    else:
        raise m.group(0)


def solve(text):
    prog = [parse_command(line) for line in text.splitlines()]

    maxbot = max(int(x[1]) for x,_,_ in prog if x[0] == 'bot')
    maxbot += 1

    maxout = max(int(x[1]) for _,x,_ in prog if x[0] == 'out')
    maxout = max(maxout, max(int(x[1]) for _,_,x in prog if x and x[0] == 'out'))
    maxout += 1

    bot_chips = [None] * 2 * maxbot
    bot_progs = list()
    outputs = [None] * maxout

    def give(target, value, chips, outputs):
        t_n, t_v = target
        if t_n == 'bot':
            i = t_v * 2
            if chips[i] is not None:
                i += 1
            chips[i] = value
        elif t_n == 'out':
            outputs[t_v] = value

    for src,t1,t2 in prog:
        src_n, src_v = src
        if src_n == 'val':
            give(t1, src_v, bot_chips, outputs)
        elif src_n == 'bot':
            bot_progs.append((src_v, t1, t2))

    has_chips = True
    while (has_chips):
        has_chips = False

        old_bot_chips = list(bot_chips)

        for botid,t1,t2 in bot_progs:
            chip_index = botid * 2

            chips = old_bot_chips[chip_index: chip_index + 2]

            if chips[0] is not None and chips[1] is not None:
                has_chips = True

                lo, hi = sorted(chips)
                bot_chips[botid * 2] = None
                bot_chips[botid * 2 + 1] = None

                give(t1, lo, bot_chips, outputs)
                give(t2, hi, bot_chips, outputs)

    return outputs[0] * outputs[1] * outputs[2]


def test():
    assert parse_target('bot 18') == ('bot', 18)
    assert parse_target('output 17') == ('out', 17)

    assert parse_command('value 5 goes to bot 2') == (('val', 5), ('bot', 2), None)
    assert parse_command('bot 2 gives low to bot 1 and high to bot 0') == (('bot', 2), ('bot', 1), ('bot', 0))
    assert parse_command('bot 0 gives low to output 2 and high to output 0') == (('bot', 0), ('out', 2), ('out', 0))

    problem = """
value 5 goes to bot 2
bot 2 gives low to bot 1 and high to bot 0
value 3 goes to bot 1
bot 1 gives low to output 1 and high to bot 0
bot 0 gives low to output 2 and high to output 0
value 2 goes to bot 2
""".strip()

    assert solve(problem) == 30

def getinput():
    import fileinput
    with fileinput.input() as f:
        return ''.join(f).strip()


if __name__ == '__main__':
    # test()

    print(solve(getinput()))
