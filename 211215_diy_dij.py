import logging
from base import Base
import numpy as np


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n1319128137\n1359912421\n3125421639\n1293138521\n2311944581': 40
        }

    def pre_treat(self, inp_):
        return np.array([
            [int(c) for c in l]
            for l in inp_.split('\n') if l
        ])

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        p2i = lambda x, y: y * inp_.shape[0] + x
        i2p = lambda x: (x % inp_.shape[0], x // inp_.shape[1])
        cost = lambda x: inp_[x % inp_.shape[0]][x // inp_.shape[1]]
        neigh = lambda x, y: [p2i(a, b) for a, b in [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                              if a >= 0 and b >= 0 and a < inp_.shape[0] and b < inp_.shape[1]]
        pred = [-1 for _ in range(inp_.shape[0] * inp_.shape[1])]
        dist = [-1 for _ in range(inp_.shape[0] * inp_.shape[1])]
        queue = [0]
        dist[p2i(0, 0)] = 0

        # Keeps track of unprocessed nodes and acts as a 
        queue = [t for t in range(inp_.shape[0] * inp_.shape[1])]

        while queue:
            queue = sorted(queue, key=lambda x: (dist[x] < 0, dist[x]), reverse=True)
            v = queue.pop()
            for n in neigh(*i2p(v)):
                if n < 0 or n >= len(dist):
                    continue
                if dist[n] < 0 or dist[v] + cost(n) < dist[n]:
                    dist[n] = dist[v] + cost(n)
                    pred[n] = v
        return dist[-1]




class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n1319128137\n1359912421\n3125421639\n1293138521\n2311944581': 40
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        pass


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
