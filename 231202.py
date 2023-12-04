import logging
from base import Base

class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""": 8
        }

    def pre_treat(self, inp_):
        inp_ = [l.split(':')[1] for l in inp_.split('\n') if l]
        inp_ = [[[e.strip().split()[::-1] for e in s.split(',')] for s in l.split(';')] for l in inp_]
        inp_ = [[{c: int(i) for c, i in s} for s in g] for g in inp_]
        return inp_

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        max_ = {'red': 12, 'green': 13, 'blue': 14}
        accu = 0
        for i, g in enumerate(inp_):
            i += 1

            if all(all(s.get(k, 0) <= max_[k] for k in max_) for s in g):
                accu += i
        return accu


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green""": 2286
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        accu = 0
        for g in inp_:
            # What is the max value for each color ?
            max_ = g[0]
            for s in g[1:]:
                max_ = {
                    k: max(max_.get(k, 0), s.get(k, 0))
                    for k in ('red', 'green', 'blue')
                }
            accu += max_['red'] * max_['green'] * max_['blue']
        return accu


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
