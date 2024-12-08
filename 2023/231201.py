import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '1abc2': 12,
            'treb7uchet': 77,
            '1abc2\npqr3stu8vwx\na1b2c3d4e5f\ntreb7uchet': 142
        }

    def pre_treat(self, inp_):
        return [l for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        s = 0
        for line in inp_:
            # Keeping only numerics
            line = [c for c in line if c.isnumeric()]
            s += int(line[0] + line[-1])
        return s


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'two1nine': 29,
            'two1nine\neightwothree\nabcone2threexyz\nxtwone3four\n4nineeightseven2\nzoneight234\n7pqrstsixteen': 281
        }
        numbers = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        self.numbers = {v: str(i + 1) for i, v in enumerate(numbers)}

    def find_fst_num(self, s):
        numbers = self.numbers
        i = 0
        while i < len(s):
            if s[i].isnumeric():
                return s[i]
            elif s[i:i+3] in numbers:
                return numbers[s[i:i+3]]
            elif s[i:i+4] in numbers:
                return numbers[s[i:i+4]]
            elif s[i:i+5] in numbers:
                return numbers[s[i:i+5]]
            i += 1
        return None

    def find_lst_num(self, s):
        numbers = self.numbers
        i = len(s) - 1
        while i >= 0:
            if s[i].isnumeric():
                return s[i]
            elif s[i:i+3] in numbers:
                return numbers[s[i:i+3]]
            elif s[i:i+4] in numbers:
                return numbers[s[i:i+4]]
            elif s[i:i+5] in numbers:
                return numbers[s[i:i+5]]
            i -= 1
        return None

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        s = 0
        for line in inp_:
            # Search from right or left
            # for the first numeric or digit name
            a = self.find_fst_num(line)
            b = self.find_lst_num(line)
            s += int(a + b)
        return s


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
