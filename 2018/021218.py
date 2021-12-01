from base import Base
from collections import Counter
from itertools import combinations


class First(Base):
    def __init__(self):
        super(First, self).__init__()
        self.examples = {
            'aabbb': 1,
            'aabb': 0,
            'bbbccc': 0,
            'abcdef\nbababc\nabbcde\nabcccd\naabcdd\nabcdee\nababab': 12,
        }

    def _solve(self, input):
        input = input.split('\n')
        res = []
        for box_id in input:
            c = Counter(box_id)
            res += list(set(v for v in c.values() if v in [2, 3]))

        c = Counter(res)
        return c[2] * c[3]


class Second(Base):
    def __init__(self):
        super(Second, self).__init__()
        self.examples = {
            'abcde\nfghij\nklmno\npqrst\nfguij\naxcye\nwvxyz': 'fgij'
        }

    def _solve(self, input):
        input = input.split('\n')
        for a, b in combinations(input, 2):
            hamming = sum(map(lambda x: x[0] == x[1], zip(a, b)))
            if hamming == len(a) - 1:
                return ''.join([c for c, d in zip(a, b) if c == d])
        return None


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
        solver = Second()
    else:
        solver = First()
    if args.test:
        solver.test_all()
    else:
        solver.solve()
