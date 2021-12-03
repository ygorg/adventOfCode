import logging
from base import Base
from collections import Counter


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010': 198
        }

    def pre_treat(self, inp_):
        return [l for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        gamma = ''.join(Counter(e).most_common(1)[0][0] for e in zip(*inp_))
        epsilon = ''.join('0' if e == '1' else '1' for e in gamma)
        return int(gamma, 2) * int(epsilon, 2)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '00100\n11110\n10110\n10111\n10101\n01111\n00111\n11100\n10000\n11001\n00010\n01010': 230
        }

    def _solve(self, inp_):
        inp_ = First.pre_treat(self, inp_)

        candidates = inp_.copy()
        i = 0
        while len(candidates) != 1:
            c = Counter(e[i] for e in candidates)
            common_bit = '0' if c['0'] > c['1'] else '1'
            candidates = [c for c in candidates if c[i] == common_bit]
            i += 1
        oxygen = candidates[0]

        candidates = inp_.copy()
        i = 0
        while len(candidates) != 1:
            c = Counter(e[i] for e in candidates)
            common_bit = '0' if c['0'] <= c['1'] else '1'
            candidates = [c for c in candidates if c[i] == common_bit]
            i += 1
        co2 = candidates[0]
        print(oxygen, co2)
        return int(oxygen, 2) * int(co2, 2)



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
