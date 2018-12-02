import re
import sys


class Base:
    def __init__(self):
        og_file = sys.argv[0]
        file_input = re.sub(r'\.py$', r'_input.txt', og_file)
        with open(file_input) as f:
            self.input = f.read()

    def _solve(self, input):
        raise NotImplementedError

    def solve(self, input=None):
        if input is None:
            input = self.input
        res = self._solve(input)
        print('Input answer : {}'.format(res))

    def test_all(self):
        valid_example = 0
        for example, solution in self.examples.items():
            res = self._solve(example)
            valid_example += 1 if res == solution else 0
            print('{} -> {} : {} {}'.format(
                example.replace('\n', '\\n'), res, solution,
                'O' if res == solution else 'X'))

        print('{}/{} good answer'.format(valid_example, len(self.examples)))


base_script = """from base import Base


class First(Base):
    def __init__(self):
        super(First, self).__init__()
        self.examples = {
            '': 0
        }

    def _solve(self, input):
        pass


class Second(Base):
    def __init__(self):
        super(Second, self).__init__()
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
        solver = Second()
    else:
        solver = First()
    if args.test:
        solver.test_all()
    else:
        solver.solve()
"""

if __name__ == '__main__':
    import argparse

    def arguments():
        parser = argparse.ArgumentParser(description='Script desc')
        parser.add_argument(
            'day', type=int, help='Day to create')
        args = parser.parse_args()
        return args

    args = arguments()

    base_name = '{:0>2}1218'.format(args.day)

    with open(base_name + '.py', 'w') as f:
        f.write(base_script)

    with open(base_name + '_input.txt', 'w') as f:
        f.write('')
