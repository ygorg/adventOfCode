from base import Base
import re
import numpy as np


def iter_claims(claims):
    claim_regex = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')
    for claim in claims:
        yield list(map(int, claim_regex.search(claim).groups()))


class First(Base):
    def __init__(self):
        super(First, self).__init__()
        self.examples = {
            '#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2': 4
        }

    def _solve(self, input):
        input = input.split('\n')
        fabric = np.zeros((1000, 1000))
        for claim in iter_claims(input):
            i, x, y, w, h = claim
            fabric[x:x + w, y:y + h] += 1

        return (fabric >= 2).sum()


class Second(Base):
    def __init__(self):
        super(Second, self).__init__()
        self.examples = {
            '#1 @ 1,3: 4x4\n#2 @ 3,1: 4x4\n#3 @ 5,5: 2x2': 3
        }

    def _solve(self, input):
        input = input.split('\n')
        fabric = np.zeros((1000, 1000), dtype=np.int64)
        available_claims = set()
        for claim in iter_claims(input):
            i, x, y, w, h = claim
            area = fabric[x:x + w, y:y + h]
            if area.sum() == 0:
                available_claims |= {i}
            else:
                available_claims -= set(area.reshape(-1).tolist())
            fabric[x:x + w, y:y + h] = i

        return list(available_claims)[0]


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
