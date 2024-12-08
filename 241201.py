import logging
from base import Base

from collections import Counter


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '''3   4
4   3
2   5
1   3
3   9
3   3''': 11
        }

    def pre_treat(self, inp_):
        inp_ = [list(map(int, l.split('   '))) for l in inp_.split('\n') if l]
        left, right = list(zip(*inp_))
        return left, right

    def _solve(self, inp_):
        left, right = self.pre_treat(inp_)
        left = sorted(left)
        right = sorted(right)
        return sum(abs(b - a) for a, b in zip(left, right))


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '''3   4
4   3
2   5
1   3
3   9
3   3''': 31
        }

    def _solve(self, inp_):
        left, right = self.pre_treat(inp_)
        right = Counter(right)
        return sum(n * right[n] for n in left)


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
