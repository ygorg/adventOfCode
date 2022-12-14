import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '6,10\n0,14\n9,10\n0,3\n10,4\n4,11\n6,0\n6,12\n4,1\n0,13\n10,12\n3,4\n3,0\n8,4\n1,10\n2,14\n8,10\n9,0\n\nfold along y=7\nfold along x=5': 17
        }

    def pre_treat(self, inp_):
        dots, folds = inp_.strip().split('\n\n')
        dots = [tuple(map(int, l.split(','))) for l in dots.split('\n')]
        folds = [(l[11], int(l[13:])) for l in folds.split('\n')]
        return dots, folds

    def _solve(self, inp_):
        dots, folds = self.pre_treat(inp_)
        d, p = folds[0]
        for i in range(len(dots)):
            x, y = dots[i]
            if d == 'y' and y > p:
                dots[i] = (x, 2 * p - y)
            if d == 'x' and x > p:
                dots[i] = (2 * p - x, y)
        return len(set(dots))


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '6,10\n0,14\n9,10\n0,3\n10,4\n4,11\n6,0\n6,12\n4,1\n0,13\n10,12\n3,4\n3,0\n8,4\n1,10\n2,14\n8,10\n9,0\n\nfold along y=7\nfold along x=5': '0'
        }

    def _solve(self, inp_):
        dots, folds = self.pre_treat(inp_)
        for d, p in folds:
            for i in range(len(dots)):
                x, y = dots[i]
                if d == 'y' and y > p:
                    dots[i] = (x, 2 * p - y)
                if d == 'x' and x > p:
                    dots[i] = (2 * p - x, y)
        dots = set(dots)
        xs, ys = list(zip(*dots))
        tmp = [[' ' for j in range(max(xs) + 1)]
               for i in range(max(ys) + 1)]
        for x, y in zip(xs, ys):
            tmp[y][x] = 'X'
        print('\n'.join(''.join(l) for l in tmp))
        # JRZBLGKH


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
