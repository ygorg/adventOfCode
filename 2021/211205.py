import logging
from base import Base
from collections import defaultdict


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '0,9 -> 5,9\n8,0 -> 0,8\n9,4 -> 3,4\n2,2 -> 2,1\n7,0 -> 7,4\n6,4 -> 2,0\n0,9 -> 2,9\n3,4 -> 1,4\n0,0 -> 8,8\n5,5 -> 8,2': 5
        }

    def pre_treat(self, inp_):
        return [[list(map(int, p.split(','))) for p in l.split(' -> ')] for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        count = defaultdict(lambda: defaultdict(int))
        dangerous = 0
        for (xb, yb), (xe, ye) in inp_:
            if xb == xe:
                for i in range(min(yb, ye), max(yb, ye) + 1):
                    count[xb][i] += 1
                    if count[xb][i] == 2:
                        dangerous += 1
            elif yb == ye:
                for i in range(min(xb, xe), max(xb, xe) + 1):
                    count[i][yb] += 1
                    if count[i][yb] == 2:
                        dangerous += 1

        return dangerous


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '0,9 -> 5,9\n8,0 -> 0,8\n9,4 -> 3,4\n2,2 -> 2,1\n7,0 -> 7,4\n6,4 -> 2,0\n0,9 -> 2,9\n3,4 -> 1,4\n0,0 -> 8,8\n5,5 -> 8,2': 12
        }

    def _solve(self, inp_):
        inp_ = First.pre_treat(self, inp_)
        count = defaultdict(lambda: defaultdict(int))
        dangerous = 0
        for (xb, yb), (xe, ye) in inp_:
            if xb == xe:
                for i in range(min(yb, ye), max(yb, ye) + 1):
                    count[xb][i] += 1
                    if count[xb][i] == 2:
                        dangerous += 1
            elif yb == ye:
                for i in range(min(xb, xe), max(xb, xe) + 1):
                    count[i][yb] += 1
                    if count[i][yb] == 2:
                        dangerous += 1
            else:
                # Diagonal
                # Find the direction
                dx = (xe - xb) // abs(xe - xb)
                dy = (ye - yb) // abs(ye - yb)
                for i in range(abs(xe - xb)+1):
                    # For every point in that direction add 1
                    count[xb + dx * i][yb + dy * i] += 1
                    if count[xb + dx * i][yb + dy * i] == 2:
                        dangerous += 1
        return dangerous


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
