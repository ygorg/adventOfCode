import re
import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '    [D]    \n[N] [C]    \n[Z] [M] [P]\n 1   2   3 \n\nmove 1 from 2 to 1\nmove 3 from 1 to 3\nmove 2 from 2 to 1\nmove 1 from 1 to 2': 'CMZ'
        }

    def pre_treat(self, inp_):
        inp_ = [l for l in inp_.split('\n')]
        reg_instr = re.compile(r'move (\d+) from (\d+) to (\d+)')
        stacks = [[] for _
                  in range(len(inp_[0]) // 4 + 1)]
        while inp_[0][1] != '1':
            for i, idx in enumerate(range(1, len(inp_[0]), 4)):
                if inp_[0][idx] != ' ':
                    stacks[i].insert(0, inp_[0][idx])
            inp_ = inp_[1:]
        inp_ = inp_[2:]
        instr = [reg_instr.match(i).groups() for i in inp_]
        instr = [tuple(int(e) for e in i) for i in instr]
        return stacks, instr

    def exec_instr(self, stack, instr):
        n, f, t = instr
        e, stack[f - 1] = stack[f - 1][-n:], stack[f - 1][:-n]
        stack[t - 1] += e[::-1]
        return stack

    def _solve(self, inp_):
        stack, instr = self.pre_treat(inp_)
        for i in instr:
            stack, self.exec_instr(stack, i)
        return ''.join(s[-1] for s in stack)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '    [D]    \n[N] [C]    \n[Z] [M] [P]\n 1   2   3 \n\nmove 1 from 2 to 1\nmove 3 from 1 to 3\nmove 2 from 2 to 1\nmove 1 from 1 to 2': 'MCD'
        }

    def exec_instr(self, stack, instr):
        n, f, t = instr
        e, stack[f - 1] = stack[f - 1][-n:], stack[f - 1][:-n]
        stack[t - 1] += e
        return stack


if __name__ == '__main__':
    import argparse

    def arguments():
        parser = argparse.ArgumentParser(description='Script desc')
        parser.add_argument(
            '-t', '--test', action='store_true', help='Execute tests')
        parser.add_argument(
            '-s', '--second', action='store_true', help='Execute second')
        args = parser.parse_args()
        return args

    args = arguments()

    if args.second:
        solver = Second(args.test)
    else:
        solver = First(args.test)
    if args.test:
        logging.basicConfig(level=logging.DEBUG)
        solver.test_all()
    else:
        logging.basicConfig(level=logging.INFO)
        solver.solve()
