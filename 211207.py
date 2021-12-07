import logging
from base import Base
import numpy as np

class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '16,1,2,0,4,2,7,1,2,14': 37
        }

    def pre_treat(self, inp_):
        return [[int(e) for e in l.split(',')]
                for l in inp_.split('\n') if l][0]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        pos = np.array(inp_)
        
        compute_fuel = lambda dest, pos: abs(dest - pos)

        min_hpos = min(pos)
        min_fuel = abs(min_hpos - pos).sum()

        # This is not very efficient we could use a dichotomy as
        #  this is a convex function. And I think a great euristic
        #  would be to begin with the mean of all the position ?
        #  I don't if this is justifies though.
        for i in range(min(pos)+1, max(pos)):
            fuel_ = compute_fuel(i, pos).sum()
            #print(f'{i:4d} {int(fuel_-356958):6d}')
            if min_fuel > fuel_:
                min_fuel = fuel_
                min_hpos = i
        return min_fuel


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '16,1,2,0,4,2,7,1,2,14': 168
        }

    def _solve(self, inp_):
        inp_ = First.pre_treat(self, inp_)
        pos = np.array(inp_)

        compute_fuel = lambda dest, pos: ((abs(dest - pos)+1) * abs(dest - pos) / 2)

        min_hpos = min(pos)
        min_fuel = compute_fuel(min_hpos, pos).sum()
        
        for i in range(min(pos)+1, max(pos)):
            fuel_ = compute_fuel(i, pos).sum()
            #print(f'{i:4d} {int(fuel_-105461913):10f}')
            if min_fuel > fuel_:
                min_fuel = fuel_
                min_hpos = i
        return min_fuel


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
