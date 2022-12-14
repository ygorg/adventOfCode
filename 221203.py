import logging
from base import Base
from more_itertools import grouper


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'vJrwpWtwJgWrhcsFMMfFFhFp\njqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\nPmmdzqPrVvPwwTWBwg\nwMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\nttgJtRGJQctTZtZT\nCrZsJsPPZsGzwwsLwLmpwMDw': 157
        }

    def pre_treat(self, inp_):
        return [(l[:int(len(l) / 2)], l[int(len(l) / 2):])
                for l in inp_.split('\n') if l]

    def priority(self, t):
        if t.islower():
            return ord(t) - ord('a') + 1
        else:
            return ord(t) - ord('A') + 27

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        inp_ = [list(set(l) & set(r)) for l, r in inp_]
        return sum(self.priority(e[0]) for e in inp_)

class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'vJrwpWtwJgWrhcsFMMfFFhFp\njqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL\nPmmdzqPrVvPwwTWBwg\nwMqvLMZHhHMvwLHjbvcjnnSBnvTQFn\nttgJtRGJQctTZtZT\nCrZsJsPPZsGzwwsLwLmpwMDw': 70
        }

    def pre_treat(self, inp_):
        return [set(l) for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        inp_ = [list(g[0].intersection(*g[1:])) for g in grouper(inp_, 3)]
        return sum(self.priority(e[0]) for e in inp_)


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
