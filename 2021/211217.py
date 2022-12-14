import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'target area: x=20..30, y=-10..-5': 45,
            'target area: x=6..10, y=-10..-5': 45,
            'target area: x=70..96, y=-179..-124': 15931
        }

    def step(self, pos, vel):
        return (
            (pos[0] + vel[0], pos[1] + vel[1]),
            (vel[0] + (-1 if vel[0] > 0 else 0), vel[1] - 1)
        )

    def collision(self, pos, sq):
        x, y = pos
        x_a, x_b, y_a, y_b = sq
        return x >= x_a and x <= x_b and y >= y_a and y <= y_b

    def too_far(self, pos, sq):
        x_a, x_b, y_b, y_a = sq
        x, y = pos
        return x > x_b or y < y_b

    def get_pos(self, vel, tar):
        # For graphical interface
        pos = (0, 0)
        hist = []
        while not self.too_far(pos, tar):
            pos, vel = self.step(pos, vel)
            hist.append(pos)
        pos, vel = self.step(pos, vel)
        hist.append(pos)
        return hist

    def pre_treat(self, inp_):
        x, y = inp_[13:].split(', ')
        return tuple(map(int, (*x[2:].split('..'), *y[2:].split('..'))))

    def _solve(self, inp_):
        tar = self.pre_treat(inp_)
        x_a, x_b, y_b, y_a = tar
        global_max = -1
        for i in range(x_b + 1):
            for j in range(abs(y_b) + 1):
                pos = (0, 0)
                vel = (i, j)
                tmp_max = -1
                while not self.too_far(pos, tar):
                    pos, vel = self.step(pos, vel)
                    tmp_max = max(tmp_max, pos[1])
                    if self.collision(pos, tar):
                        logging.debug('Collision ! {}'.format(tmp_max))
                        global_max = max(tmp_max, global_max)
                        break
        return global_max


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'target area: x=20..30, y=-10..-5': 112,
            'target area: x=6..10, y=-10..-5': 0,
            'target area: x=70..96, y=-179..-124': 2555
        }

    def _solve(self, inp_):
        tar = self.pre_treat(inp_)
        x_a, x_b, y_b, y_a = tar
        nb_col = 0
        for i in range(x_b + 1):
            for j in range(y_b - 1, -y_b + 1):
                pos = (0, 0)
                vel = (i, j)
                while not self.too_far(pos, tar):
                    pos, vel = self.step(pos, vel)
                    if self.collision(pos, tar):
                        nb_col += 1
                        logging.debug('Collision ! {}'.format(nb_col))
                        break
        return nb_col


if __name__ == '__main__':
    import argparse

    def arguments():
        parser = argparse.ArgumentParser(description='Script desc')
        parser.add_argument(
            '-t', '--test', action='store_true', help='Execute tests')
        parser.add_argument(
            '-s', '--second', action='store_true', help='Execute second')
        parser.add_argument(
            '-d', '--debug', action='store_true', help='Print debug logging')
        args = parser.parse_args()
        return args

    args = arguments()

    if args.second:
        solver = Second(args.test)
    else:
        solver = First(args.test)
    if args.test:
        logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG)
        solver.test_all()
    else:
        logging.basicConfig(level=logging.INFO if not args.debug else logging.DEBUG)
        solver.solve()
