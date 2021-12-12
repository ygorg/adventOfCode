import logging
from base import Base
import networkx as nx
from collections import defaultdict, Counter


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'start-A\nstart-b\nA-c\nA-b\nb-d\nA-end\nb-end': 10,
            'dc-end\nHN-start\nstart-kj\ndc-start\ndc-HN\nLN-dc\nHN-end\nkj-sa\nkj-HN\nkj-dc': 19,
            'fs-end\nhe-DX\nfs-he\nstart-DX\npj-DX\nend-zg\nzg-sl\nzg-pj\npj-he\nRW-he\nfs-DX\npj-RW\nzg-RW\nstart-pj\nhe-WI\nzg-he\npj-fs\nstart-RW': 226
        }

    def pre_treat(self, inp_):
        edges = [l.split('-') for l in inp_.split('\n') if l]
        g = nx.Graph()
        g.add_edges_from(edges)
        return g

    def rec(self, path, current, G):
        path = path.copy() + [current]
        neighbors = list(G.neighbors(current))
        neighbors = [
            n for n in neighbors
            if n.isupper() or (n.islower() and n not in path)
        ]
        if current == 'end':
            return [path]
        elif not neighbors:
            return []
        paths = []
        for n in neighbors:
            paths += self.rec(path, n, G)
        return paths

    def _solve(self, inp_):
        g = self.pre_treat(inp_)
        paths = self.rec([], 'start', g)
        return len(paths)



class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'start-A\nstart-b\nA-c\nA-b\nb-d\nA-end\nb-end': 36,
            'dc-end\nHN-start\nstart-kj\ndc-start\ndc-HN\nLN-dc\nHN-end\nkj-sa\nkj-HN\nkj-dc': 103,
            'fs-end\nhe-DX\nfs-he\nstart-DX\npj-DX\nend-zg\nzg-sl\nzg-pj\npj-he\nRW-he\nfs-DX\npj-RW\nzg-RW\nstart-pj\nhe-WI\nzg-he\npj-fs\nstart-RW': 3509
        }

    def rec(self, path, current, G):
        path = path.copy() + [current]
        neighbors = list(G.neighbors(current))
        c = Counter(e for e in path if e.islower())
        can_another = not any(e > 1 for e in c.values())
        neighbors = [
            n for n in neighbors
            if n != 'start' and (n.isupper() or (n.islower() and (can_another or n not in path)))
        ]

        if current == 'end':
            return [path]
        elif not neighbors:
            return []
        paths = []
        for n in neighbors:
            paths += self.rec(path, n, G)
        return paths

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
