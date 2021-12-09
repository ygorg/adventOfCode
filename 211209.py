import logging
from base import Base
import numpy as np


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '2199943210\n3987894921\n9856789892\n8767896789\n9899965678': 15
        }

    def pre_treat(self, inp_):
        return [[int(c) for c in l] for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        height = np.array(inp_)
        mask = np.ones_like(height).astype(bool)

        tmp = np.concatenate(([[9]] * height.shape[0], height[:, :-1]), axis=1)
        mask = ((tmp - height) > 0) & mask
        tmp = np.concatenate((height[:, 1:], [[9]] * height.shape[0]), axis=1)
        mask = ((tmp - height) > 0) & mask
        tmp = np.concatenate(([[9] * height.shape[1]], height[:-1, :]), axis=0)
        mask = ((tmp - height) > 0) & mask
        tmp = np.concatenate((height[1:, :], [[9] * height.shape[1]]), axis=0)
        mask = ((tmp - height) > 0) & mask

        return np.where(mask == True, height + 1, 0).sum()



class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '2199943210\n3987894921\n9856789892\n8767896789\n9899965678': 1134
        }

    def _solve(self, inp_):
        inp_ = First.pre_treat(self, inp_)
        height = np.array(inp_)
        mask = np.ones_like(height).astype(bool)

        tmp = np.concatenate(([[9]] * height.shape[0], height[:, :-1]), axis=1)
        mask = ((tmp - height) > 0) & mask
        tmp = np.concatenate((height[:, 1:], [[9]] * height.shape[0]), axis=1)
        mask = ((tmp - height) > 0) & mask
        tmp = np.concatenate(([[9] * height.shape[1]], height[:-1, :]), axis=0)
        mask = ((tmp - height) > 0) & mask
        tmp = np.concatenate((height[1:, :], [[9] * height.shape[1]]), axis=0)
        mask = ((tmp - height) > 0) & mask
        xs, ys = np.where(mask == True)

        basins_count = []
        for i, (x, y) in enumerate(zip(xs, ys)):
            # For each minima:
            pile = [(x, y)]
            basins_count.append(0)
            while pile:
                x, y = pile.pop()
                if (x < 0 or x >= height.shape[0] or
                    y < 0 or y >= height.shape[1]):
                    continue
                if height[x, y] < 0:
                    continue
                height[x, y] = -1
                basins_count[-1] += 1
                for j in (1, -1):
                    if (0 <= x + j < height.shape[0]
                        and height[x + j, y] != 9
                        and height[x + j, y] >= height[x, y]):
                        pile.append((x + j, y))
                    if (0 <= y + j < height.shape[1]
                        and height[x, y + j] != 9
                        and height[x, y + j] >= height[x, y]):
                        pile.append((x, y + j))

        basins_count = sorted(basins_count, reverse=True)
        print(basins_count)
        a, b, c = basins_count[:3]
        # 1017792
        return a * b * c


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
