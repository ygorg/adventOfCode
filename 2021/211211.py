import logging
from base import Base
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def display(i):
    sns.heatmap(i, vmin=0, vmax=9, square=True, annot=True)#, cmap=sns.color_palette("green:red", as_cmap=True))
    plt.show(block=False)
    input()
    plt.close()


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '5483143223\n2745854711\n5264556173\n6141336146\n6357385478\n4167524645\n2176841721\n6882881134\n4846848554\n5283751526': 1656
        }

    def pre_treat(self, inp_):
        return np.array([[int(e) for e in l] for l in inp_.split('\n') if l])

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        nb_light = 0
        for i in range(100):
            #display(inp_)
            inp_ += 1
            # Already popped
            mask = np.ones_like(inp_, dtype=np.bool_)
            while (inp_ > 9).any():
                x, y = np.where(inp_ > 9)
                x, y = x[0], y[0]

                # Pop
                mask[x][y] = False
                inp_[x][y] = 0
                nb_light += 1
                #display(inp_)

                tmp_mask = np.zeros_like(inp_, dtype=np.bool)
                xp, yp = max(x - 1, 0), max(y - 1, 0)
                xg, yg = min(x + 2, inp_.shape[0]), min(y + 2, inp_.shape[1])
                tmp_mask[xp:xg, yp:yg] = True
                # Increase only unpopped and in area
                inp_ = np.where(tmp_mask & mask, inp_ + 1, inp_)
                #display(inp_)
                # Add new ready to pop
        return nb_light


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '5483143223\n2745854711\n5264556173\n6141336146\n6357385478\n4167524645\n2176841721\n6882881134\n4846848554\n5283751526': 195
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        for i in range(1500):
            inp_ += 1
            # Already popped
            mask = np.ones_like(inp_, dtype=np.bool_)
            while (inp_ > 9).any():
                x, y = np.where(inp_ > 9)
                x, y = x[0], y[0]

                # Pop
                mask[x][y] = False
                inp_[x][y] = 0

                tmp_mask = np.zeros_like(inp_, dtype=np.bool)
                xp, yp = max(x - 1, 0), max(y - 1, 0)
                xg, yg = min(x + 2, inp_.shape[0]), min(y + 2, inp_.shape[1])
                tmp_mask[xp:xg, yp:yg] = True
                # Increase only unpopped and in area
                inp_ = np.where(tmp_mask & mask, inp_ + 1, inp_)
                # Add new ready to pop
            #if i % 20 == 0:
            #    print(i)
            #    display(inp_)
            # Really dirty but quick and easy
            if mask.sum() == 0:
                return i + 1
        return 0


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
        #logging.basicConfig(level=logging.DEBUG)
        solver.test_all()
    else:
        logging.basicConfig(level=logging.INFO)
        solver.solve()
