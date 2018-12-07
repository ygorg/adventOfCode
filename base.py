import re
import sys
import os


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


base_script = """import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '': 0
        }

    def _solve(self, input):
        pass


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
    script_name = base_name + '.py'
    input_name = base_name + '_input.txt'

    if not os.path.isfile(script_name):
        with open(script_name, 'w') as f:
            f.write(base_script)
    else:
        print('{} already exists'.format(base_script))

    if not os.path.isfile(input_name):
        with open(input_name, 'w') as f:
            f.write('')
    else:
        print('{} already exists'.format(input_name))
