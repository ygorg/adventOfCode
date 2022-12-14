import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '199\n200\n208\n210\n200\n207\n240\n269\n260\n263': 7
        }

    def pre_treat(self, radar):
        return [int(l) for l in radar.split('\n')]

    def _solve(self, radar):
        radar = self.pre_treat(radar)
        return sum((radar[i] - radar[i - 1]) > 0 for i in range(1, len(radar)))


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '199\n200\n208\n210\n200\n207\n240\n269\n260\n263': 5
        }

    def _solve(self, radar):
        radar = First.pre_treat(self, radar)
        radar = [radar[i] + radar[i - 1] + radar[i + 1]
                 for i in range(1, len(radar) - 1)]
        return sum((radar[i] - radar[i - 1]) > 0 for i in range(1, len(radar)))


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
