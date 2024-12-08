import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.cards = {k: i for i, k in enumerate('23456789TJQKA')}
        self.cards[0] = 0

        self.examples = {
            """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""": 6440
        }

    def pre_treat(self, inp_):
        inp_ = [l.split(' ') for l in inp_.split('\n') if l]
        # Transform all cards into numeric
        inp_ = [([self.cards[c] for c in h], int(b)) for h, b in inp_]
        return inp_

    def _solve(self, inp_):
        from collections import Counter
        hands = self.pre_treat(inp_)

        # We only need the best 2 combinations to sort the hands
        # Either 5; 4-1; 3-2; 3-1; 2-2; 2-1; 1-1
        hands = [(sorted(Counter(h).values(), reverse=True)[:2], h, b) for h, b in hands]

        hands = sorted(hands, key=lambda h: (h[0], h[1]))

        winnings = [(i + 1) * b for i, (_, _, b) in enumerate(hands)]

        return sum(winnings)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.cards = {k: i for i, k in enumerate('J23456789TQKA')}
        self.examples = {
            """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483""": 5905
        }

    def _solve(self, inp_):
        from collections import Counter
        hands = self.pre_treat(inp_)

        # We only need the best 2 combinations to sort the hands
        # Either 5; 4-1; 3-2; 3-1; 2-2; 2-1; 1-1

        def process(h):
            count = Counter(h)
            nb_j = count[self.cards['J']]
            count = [c for k, c in count.most_common() if k != self.cards['J']][:2]
            count = count + [0] * (2 - len(count))
            count[0] += nb_j
            return count, h

        hands = [(*process(h), b) for h, b in hands]
        hands = sorted(hands, key=lambda h: (h[0], h[1]))

        winnings = [(i + 1) * b for i, (_, _, b) in enumerate(hands)]

        return sum(winnings)


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
