import re
import logging

from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))': 161
        }

    def pre_treat(self, inp_):
        return inp_

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        res = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', inp_)
        return sum(int(a) * int(b) for a, b in res)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))": 48
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        inst = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)|d(o)\(\)|do(n)\'t\(\)', inp_)
        do = True
        res = 0
        for a, b, y, n in inst:
            if y:
                do = True
            elif n:
                do = False
            else:
                if do:
                    res += int(a) * int(b)
        return res


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
