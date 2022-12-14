import logging
from base import Base
import numpy as np
from scipy.signal import convolve2d


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#\n\n#..#.\n#....\n##..#\n..#..\n..###': 35
        }

    def pre_treat(self, inp_):
        inp_ = inp_.split('\n')
        trs = lambda c: 0 if c == '.' else 1
        alg = [trs(c) for c in inp_[0]]
        img = np.array([[trs(c) for c in line] for line in inp_[2:]])
        return alg, img

    def step(self, img, alg, i):
        # Create convolution kernel
        mat = np.array([1, 2, 4, 8, 16, 32, 64, 128, 256]).reshape((3, 3))
        # Apply convolution
        cval = 0
        # Whoopsies I kinda cheated for this: I went to see other's solutions
        if alg[0] == 1 and i % 2 == 1:
            cval = 1
        tmp = convolve2d(img, mat, fillvalue=cval)
        # Get pixels from convolved matrix to get next image
        return np.array([[alg[x] for x in r] for r in tmp])

    def pprint(self, img):
        conv = ['.', '#']
        print('\n'.join((''.join(conv[i] for i in r) for r in img)))

    def _solve(self, inp_):
        alg, img = self.pre_treat(inp_)
        for i in range(2):
            img = self.step(img, alg, i)
        return img.sum()


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#\n\n#..#.\n#....\n##..#\n..#..\n..###': 3351
        }

    def _solve(self, inp_):
        alg, img = self.pre_treat(inp_)
        for i in range(50):
            img = self.step(img, alg, i)
        return img.sum()


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
