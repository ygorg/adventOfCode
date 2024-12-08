import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""": 13
        }

    def pre_treat(self, inp_):
        return [
            [[int(e) for e in lst.split(' ') if e]
             for lst in l.split(': ')[-1].split(' | ')
            ] for l in inp_.split('\n') if l
        ]

    def matching_numbers(self, card):
        return len(set(card[0]) & set(card[1]))

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        points = 0
        for card in inp_:
            matching = self.matching_numbers(card)
            if matching:
                points += 2**(len(matching) - 1)
        return points


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""": 30
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        nb_cards = [1] * len(inp_)
        for i, card in enumerate(inp_):
            matching = self.matching_numbers(card)
            for j in range(min(len(inp_), i+1), min(len(inp_), i+matching+1)):
                nb_cards[j] += nb_cards[i]
        return sum(nb_cards)


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
