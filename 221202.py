import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'A Y\nB X\nC Z': 15
        }

    def pre_treat(self, inp_):
        data = [l.split(' ') for l in inp_.split('\n') if l]
        data = [(ord(o) - ord('A'), ord(p) - ord('X'))
                for o, p in data]
        return data

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        score = 0
        # 0 is rock, 1 is paper, 2 is cisors
        # if i am 1 above the oponnent mod 3 then I win
        # r p -> 0 1 -> win
        # p c -> 1 2 -> win
        # c r -> 2 0 -> win
        for opp, pla in inp_:
            score += pla + 1
            if opp == pla:
                score += 3
            elif (opp + 1) % 3 == pla:
                score += 6
        return score


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'A Y\nB X\nC Z': 12
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        score = 0
        # 0 is lose, 1 is draw, 2 is win
        # if i play 2+X above the oponnent mod 3 then
        #  i get the right outcome
        # 1 l -> 1 + 2+0mod3 -> 3mod3 -> 0
        # 1 d -> 1 + 2+1mod3 -> 4mod3 -> 1
        # 1 w -> 1 + 2+2mod3 -> 5mod3 -> 2
        for opp, out in inp_:
            pla = (opp + 2 + out) % 3
            score += pla + 1 + out * 3
        return score


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
