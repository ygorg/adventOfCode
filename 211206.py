import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '3,4,3,1,2': 5934,
            '1': 1401
        }

    def pre_treat(self, inp_):
        return [[int(e) for e in l.split(',')]
                for l in inp_.split('\n') if l][0]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        fishes = [0 for _ in range(9)]
        for life_expectancy in inp_:
            fishes[life_expectancy] += 1
        i = 0
        print(f'{i:2d} {sum(fishes):8d} {fishes}')
        for i in range(80):
            will_reproduce = fishes.pop(0)
            fishes.append(will_reproduce)
            fishes[6] += will_reproduce
            print(f'{i+1:2d} {sum(fishes):8d} {fishes}')
        return sum(fishes)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '3,4,3,1,2': 26984457539
        }

    def _solve(self, inp_):
        # We could also compute the number of fishes 1 fish produces when
        # beggining at 6 like answer[day] = nb_fish and then assign for each
        # fish `answer[256-(fish_age-7)]` something like this
        # But in order to compute this we still need to compute avery 256
        # iterations so won't gain anything from the actual method
        # Note: each fish at the beginning is a mathematics sequence that
        # I don't know how to model, we could try to go back in time and
        # see what were the original set of fishes that existed and then compute
        # in O(1) if the sequence is modeled, because each one of these fish is
        # a particular sequence. And this could maybe be done because the fishes
        # do not interact with each other.
        inp_ = First.pre_treat(self, inp_)
        fishes = [0 for _ in range(9)]
        for life_expectancy in inp_:
            fishes[life_expectancy] += 1
        i = 0
        print(f'{i:2d} {sum(fishes):8d} {fishes}')
        for i in range(256):
            will_reproduce = fishes.pop(0)
            fishes.append(will_reproduce)
            fishes[6] += will_reproduce
            print(f'{i+1:2d} {sum(fishes):8d} {fishes}')
        return sum(fishes)


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
