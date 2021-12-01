import logging
from base import Base
import re
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

example_ = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>"""


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            example_: 3
        }

    def parse(self, input):
        input = input.split('\n')
        line_reg = re.compile(r'position=<\s*(-?\d+),\s*(-?\d+)> velocity=<\s*(-?\d+),\s*(-?\d+)>')
        points = []
        for line in input:
            points.append(list(map(int, line_reg.match(line).groups())))
        return points

    def create_image(self, points):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]

        min_x = min(xs)
        min_y = min(ys)
        width = abs(max(xs) - min_x)
        length = abs(max(ys) - min_y)
        img = np.zeros((width + 1, length + 1))
        for x, y in points:
            img[x - min_x, y - min_y] = 1
        return img

    def points_at_t(self, points, t=0):
        """Returns the point list at time t given their speed

        :param points: list of points with speed
        :type points: list of tuple ((x, y, vx, vy))
        :param t: time, defaults to 0
        :type t: number, optional
        """
        return [(x + vx * t, y + vy * t)
                for x, y, vx, vy in points]

    def connex_components(self, points):
        """Computes the connex components of a list of point. Two objects are
           connected if they "touch" each other

        :param points: list of points
        :type points: list of tuple (x, y)
        :returns: A lost of connex components
        :rtype: {list of list of tuple (x, y)}
        """
        def next_to(x, y):
            """Return a function computing whether the point given "touches"
               another

            :param x: x position
            :type x: int
            :param y: y position
            :type y: int
            :returns: A function
            :rtype: {(x, y) -> bool}
            """
            return lambda e: (abs(e[0] - x) == 1 and e[1] == y)\
                or (abs(e[1] - y) == 1 and e[0] == x)

        def next_to_l(x, y, l):
            """Applies next_to to a list of

            :param l: List of points
            :type l: list of tuple (x, y)
            :returns: Whether of not a point of `l` touches (x, y)
            :rtype: {bool}
            """
            return any(map(next_to(x, y), l))

        components = []
        # For each point
        for x, y in points:
            n = []
            for i, c in enumerate(components):
                # Is (x, y) next to the component c
                if next_to_l(x, y, c):
                    n.append(i)
            # Create a new component
            new_c = [(x, y)]
            for i in n[::-1]:  # Looping backward as we remove elements from the list
                # Merge every components (x, y) is next to
                new_c += components[i]
                # Remove the merged componen
                del components[i]
            components.append(new_c)
        return components

    def _solve(self, input):
        points = self.parse(input)

        def dims(points):
            xs = [e[0] for e in points]
            w = abs(max(xs) - min(xs))
            ys = [e[1] for e in points]
            h = abs(max(ys) - min(ys))
            return w + h

        # Kinda do it by hand by changing the range

        # We use features like the number of connex components and the size of
        # the box containing every points to find a minimum of these features
        # the timesetp minimizing any of these two feature is the timestep we
        # are searching for

        # c_min = len(points)
        d_min = dims(points)
        for i in tqdm(range(10500, 10600)):
            points_t = self.points_at_t(points, t=i)
            # c = len(self.connex_components(points_t))
            d = dims(points_t)
            if d < d_min:
                d_min = d
                print((i, d))
                img = self.create_image(points_t)
                plt.imshow(img)
                plt.show()


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '': 0
        }

    def _solve(self, input):
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
