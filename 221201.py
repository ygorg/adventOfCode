import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000': 24000
        }

    def pre_treat(self, inp_):
        data = [[]]
        for l in inp_.split('\n'):
            if not l:
                data.append([])
            else:
                data[-1].append(int(l))
        return data

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        return max(sum(e) for e in inp_)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '1000\n2000\n3000\n\n4000\n\n5000\n6000\n\n7000\n8000\n9000\n\n10000': 45000
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        return sum(sorted(sum(e) for e in inp_)[-3:])


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
