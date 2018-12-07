import math
import logging
from base import Base
import numpy as np
from collections import Counter

def norm(u):
    return math.sqrt(u[0] * u[0] + u[1] * u[1])


def dot(u, v):
    return u[0] * v[0] + u[1] * v[1]


def cos(u, v):
    try:
        return 1 - (dot(u, v) / (norm(u) * norm(v)))
    except ZeroDivisionError:
        return 1


def diff(u, v):
    return (u[0] - v[0], u[1] - v[1])


def jarvis(points):
    endpoint = sorted(points, key=lambda p: cos((1, 0), diff(p, (0, 0))), reverse=True)[0]  # which is guaranteed to be part of the CH(S)
    hull = list()
    while len(hull) == 0 or endpoint != hull[0]:  # wrapped around to first hull point
        max_dist = -99999
        hull.append(endpoint)
        endpoint = points[0]

        for p in points:
            if p in hull and p != hull[0]:
                continue
            before_last = hull[-2] if len(hull) > 2 else (0, 0)
            last = hull[-1]

            dist = cos(diff(before_last, last), diff(p, last))
            if (dist > max_dist):
                endpoint = p
                max_dist = dist
    return hull, [points.index(p) for p in hull]


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9': 17,
            '0, 1\n1, 4\n0, 8\n3, 7\n6, 8\n5, 1\n3, 3\n5, 5': 6
        }

    def manhattan(self, x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def _solve(self, input):
        add_a = lambda x: chr(ord('A') + x)
        points = [tuple(map(int, point.split(', ')))
                  for point in input.split('\n')]

        logging.debug({add_a(i): p for i, p in enumerate(points)})
        x_max = 1 + max(map(lambda x: x[0], points))
        y_max = 1 + max(map(lambda x: x[1], points))
        logging.info('Matrix size : {} x {}'.format(x_max, y_max))

        # Computing distance for each location and area
        distances = [self.manhattan((i, j), p) for p in points
                     for i in range(x_max) for j in range(y_max)]
        distances = np.array(distances).reshape((len(points), x_max, y_max))
        # Removing areas that are at same minimal distance from multiple locations
        mat = distances.argmin(0)
        mat[(distances == distances.min(0)).sum(0) > 1] = -1
        logging.debug(mat.T)
        # Removing infinite locations (the one on the edge of the matrix)
        edges = (set(mat[0, :]) | set(mat[-1, :]) |
                 set(mat[:, 0]) | set(mat[:, -1]))
        idx_edges = np.in1d(mat, list(edges)).reshape((x_max, y_max))
        mat[idx_edges] = -1

        logging.debug(mat.T)
        # Retrieving best area
        count = Counter(mat.reshape(-1))
        logging.info({add_a(k): v for k, v in count.items()})
        most_commons = count.most_common(n=2)
        if most_commons[0][0] == -1:
            return most_commons[1][1]
        else:
            return most_commons[0][1]


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '1, 1\n1, 6\n8, 3\n3, 4\n5, 5\n8, 9': 16
        }
        if test:
            self.min = 32
        else:
            self.min = 10000

    def _solve(self, input):
        add_a = lambda x: chr(ord('A') + x)
        points = [tuple(map(int, point.split(', ')))
                  for point in input.split('\n')]

        logging.debug({add_a(i): p for i, p in enumerate(points)})
        x_max = 1 + max(map(lambda x: x[0], points))
        y_max = 1 + max(map(lambda x: x[1], points))
        logging.info('Matrix size : {} x {}'.format(x_max, y_max))

        # Computing distance for each location and area
        distances = [self.manhattan((i, j), p) for p in points
                     for i in range(x_max) for j in range(y_max)]
        distances = np.array(distances).reshape((len(points), x_max, y_max))
        mat = distances.sum(0)
        logging.debug(mat.T)
        # Removing area that are too far
        mat = mat < self.min
        logging.debug(mat.T)

        return mat.sum()


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
