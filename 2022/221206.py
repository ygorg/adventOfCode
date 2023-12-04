import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'mjqjpqmgbljsphdztnvjfqwrcgsmlb': 7,
            'bvwbjplbgvbhsrlpgdmjqwftvncz': 5,
            'nppdvjthqldpwncqszvftbrmjlhg': 6,
            'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg': 10,
            'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw': 11
        }

    def pre_treat(self, inp_):
        return inp_.strip()

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        i = 3
        while len(set(inp_[i - 4:i])) != 4:
            i += 1
        return i


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'mjqjpqmgbljsphdztnvjfqwrcgsmlb': 19,
            'bvwbjplbgvbhsrlpgdmjqwftvncz': 23,
            'nppdvjthqldpwncqszvftbrmjlhg': 23,
            'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg': 29,
            'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw': 26
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        i = 13
        while len(set(inp_[i - 14:i])) != 14:
            i += 1
        return i


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
