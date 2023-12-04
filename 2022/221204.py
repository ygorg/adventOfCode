import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8': 2
        }

    def pre_treat(self, inp_):
        pret = lambda x: [[int(n) for n in e.split('-')] for e in x.split(',')]
        return [pret(l) for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        nb_cont = 0
        for (a, b), (c, d) in inp_:
            if (a <= c and b >= d) or (c <= a and d >= b):
                nb_cont += 1
        return nb_cont

class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '2-4,6-8\n2-3,4-5\n5-7,7-9\n2-8,3-7\n6-6,4-6\n2-6,4-8': 4
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        nb_over = 0
        for (a, b), (c, d) in inp_:
            # a or b is within c-d
            if (c <= a and a <= d) or (c <= b and b <= d):
                nb_over += 1
            # c or d is within a-b
            elif (a <= c and c <= b) or (a <= d and d <= b):
                nb_over += 1
        return nb_over


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
