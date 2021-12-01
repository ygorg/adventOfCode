from base import Base


class First(Base):
    def __init__(self):
        super(First, self).__init__()
        self.examples = {
            '+1\n+1\n+1': 3,
            '+1\n+1\n-2': 0,
            '-1\n-2\n-3': -6
        }

    def _solve(self, input):
        return sum(map(int, input.strip().split('\n')))


class Second(Base):
    def __init__(self):
        super(Second, self).__init__()
        self.examples = {
            '+1\n-1': 0,
            '+3\n+3\n+4\n-2\n-4': 10,
            '-6\n+3\n+8\n+5\n-6': 5,
            '+7\n+7\n-2\n-7\n-4': 14
        }

    def _solve(self, input):
        input = list(map(int, input.strip().split('\n')))
        seen = {0}
        i = 0
        new_number = input[0]
        while new_number not in seen:
            seen |= {new_number}
            i += 1
            new_number += input[i % len(input)]
        return new_number


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
        solver = Second()
    else:
        solver = First()
    if args.test:
        solver.test_all()
    else:
        solver.solve()
