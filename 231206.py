import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            """Time:      7  15   30
Distance:  9  40  200""": 288
        }

    def pre_treat(self, inp_):
        import re
        t, d = inp_.split('\n')
        t = re.split(r' +', t.split(':')[-1])
        t = [int(e) for e in t if e.strip()]
        d = re.split(r' +', d.split(':')[-1])
        d = [int(e) for e in d if e.strip()]
        return t, d

    def nb_ways(self, time, record):
        # Find the function (a polynom)
        import math
        a, b, c = -1, time, -record
        # f = lambda x: a * x**2 + b * x + c
        delta = b**2 - 4 * a * c
        delta = math.sqrt(delta)
        # Find the solution to the equation == 0
        x_a = (-b - delta) / (2 * a)
        x_b = (-b + delta) / (2 * a)

        nb_ways = math.floor(x_a) - math.ceil(x_b) + 1
        # Fiddle around with only considering values > 0
        # If f(x_a) == 0 then do not consider it
        #  if x_a is has no decimal part then do not consider it
        if int(x_a) == x_a:
            nb_ways -= 1
        if int(x_b) == x_b:
            nb_ways -= 1
        return nb_ways

    def _solve(self, inp_):
        time, record = self.pre_treat(inp_)
        res = 1
        for i in range(len(time)):
            res *= self.nb_ways(time[i], record[i])
        return res


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            """Time:      7  15   30
Distance:  9  40  200""": 71503
        }

    def pre_treat(self, inp_):
        inp_ = inp_.replace(' ', '')
        inp_ = super().pre_treat(inp_)
        return inp_

    def _solve(self, inp_):
        time, record = self.pre_treat(inp_)
        return self.nb_ways(time[0], record[0])


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
