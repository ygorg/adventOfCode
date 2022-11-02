import logging
from base import Base
import networkx as nx


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n1319128137\n1359912421\n3125421639\n1293138521\n2311944581': 40
        }

    def pre_treat(self, inp_):
        return [list(map(int, l)) for l in inp_.split('\n') if l]

    def create_graph(self, H, W):
        G = nx.Graph()
        for i in range(H):
            for j in range(W):
                n = i * W + j
                if i + 1 < H:
                    G.add_edge(n, n + H)
                if i - 1 >= 0:
                    G.add_edge(n, n - H)
                if j + 1 < W:
                    G.add_edge(n, n + 1)
                if j - 1 >= 0:
                    G.add_edge(n, n - 1)
        return G

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        W, H = len(inp_[0]), len(inp_)
        G = self.create_graph(H, W)
        path = nx.dijkstra_path(G, 0, H*W-1, lambda f, t, _: inp_[t//H][t%W])
        cost = 0
        for i in path[1:]:
            cost += inp_[i//H][i%W]
        return cost



class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '1163751742\n1381373672\n2136511328\n3694931569\n7463417111\n1319128137\n1359912421\n3125421639\n1293138521\n2311944581': 315
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        W, H = len(inp_[0]), len(inp_)
        W2, H2 = W*5, H*5
        G = self.create_graph(H2, W2)
        def costt(f, t, d):
            x, y = t//H2, t%W2  # between 0 - H2
            cost = inp_[x%H][y%W] -1 # le poids normal
            cost = (cost + x//H + y//W) % 9  # increased weight
            return cost+1
        path = nx.dijkstra_path(G, 0, H2*W2-1, costt)
        cost = 0
        for i in path[1:]:
            cost += costt(0, i, {})
        return cost


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
