import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2': 150
        }
        self.inst2action = {
            "forward": lambda v, x, y: (x + v, y),
            "down": lambda v, x, y: (x, y + v),
            "up": lambda v, x, y: (x, y - v)
        }

    def pre_treat(self, inp_):
        inp_ = [l.split(' ') for l in inp_.split('\n') if l]
        return [(i, int(v)) for i, v in inp_]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        x, y = 0, 0
        for inst, val in inp_:
            x, y = self.inst2action[inst](val, x, y)
        return x * y


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'forward 5\ndown 5\nforward 8\nup 3\ndown 8\nforward 2': 900
        }
        self.inst2action = {
            "forward": lambda v, x, y, a: (x + v, y + v * a, a),
            "down": lambda v, x, y, a: (x, y, a + v),
            "up": lambda v, x, y, a: (x, y, a - v)
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        x, y, a = 0, 0, 0
        for inst, val in inp_:
            x, y, a = self.inst2action[inst](val, x, y, a)
        return x * y


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
