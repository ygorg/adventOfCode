import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '0 3 6 9 12 15\n1 3 6 10 15 21\n10 13 16 21 30 45': 114
        }

    def pre_treat(self, inp_):
        inp_ = [l.split(' ') for l in inp_.split('\n') if l]
        return [[int(e) for e in l] for l in inp_]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)

        def prediction(lst):
            if all(e == 0 for e in lst):
                return lst[-1]
            tmp_lst = [lst[i+1] - lst[i] for i in range(len(lst) - 1)]
            tmp = prediction(tmp_lst)
            return lst[-1] + tmp

        res = 0
        for values in inp_:
            tmp = prediction(values)
            res += tmp
        return res



class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '0 3 6 9 12 15\n1 3 6 10 15 21\n10 13 16 21 30 45': 2
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)

        def prediction(lst):
            if all(e == 0 for e in lst):
                return lst[0]
            tmp_lst = [lst[i+1] - lst[i] for i in range(len(lst) - 1)]
            tmp = prediction(tmp_lst)
            return lst[0] - tmp

        res = 0
        for values in inp_:
            tmp = prediction(values)
            res += tmp
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
