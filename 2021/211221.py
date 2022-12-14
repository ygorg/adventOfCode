import logging
from base import Base
from itertools import product
from collections import Counter


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'Player 1 starting position: 4\nPlayer 2 starting position: 8': 739785
        }

    def pre_treat(self, inp_):
        places = [int(line.split(': ')[-1]) for line in inp_.split('\n')]
        return places

    def dice(self, m=100):
        i = 1
        while True:
            if i <= m - 3:
                yield i * 3 + 3
            else:
                yield i + (i + 1) % m + (i + 2) % m
            i += 3
            if i > m:
                i = i % m

    def step(self, places, scores, i, roll):
        places = places.copy()
        scores = scores.copy()
        places[i % 2] = (places[i % 2] + roll - 1) % 10 + 1
        scores[i % 2] += places[i % 2]
        return places, scores

    def _solve(self, inp_):
        places = self.pre_treat(inp_)
        scores = [0, 0]
        dice = self.dice()
        i = 0
        while scores[0] < 1000 and scores[1] < 1000:
            roll = next(dice)
            places, scores = self.step(places, scores, i, roll)
            i += 1
        return scores[i % 2] * i * 3


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'Player 1 starting position: 4\nPlayer 2 starting position: 8': 444356092776315
        }
        self.dice = Counter(sum(r) for r in product(*[[1, 2, 3]] * 3)).items()
        self.dice = [(sum(r), 1) for r in product(*[[1, 2, 3]] * 3)]
        self.rules = {}

    def stepp1(self, places, scores, turn=0):
        wins = [0, 0]
        scores_og = scores
        for roll, nb_occ in self.dice:
            places, scores = self.step(places, scores_og, turn % 2, roll)
            if scores[turn % 2] >= 21:
                wins[turn % 2] += nb_occ
                # print(' ' * turn + f'{roll} X')
            else:
                key = (tuple(places), tuple(scores))
                if key in self.rules:
                    w1, w2 = self.rules[key]
                else:
                    w1, w2 = self.stepp(places, scores, turn + 1)
                    if key in self.rules:
                        print('Already !?', self.rules[key] == (w1, w2))
                    self.rules[key] = (w1, w2)
                # print(' ' * turn + f'{roll} {places} {scores} {[w1, w2]}')
                wins[0] += w1
                wins[1] += w2
        return wins

    def stepp(self, places, scores, turn=0):
        # If this configuration was already played return
        key = (*places, *scores)
        if key in self.rules:
            return self.rules[key]
        # If someone wins return
        if scores[0] >= 21:
            return (1, 0)
        if scores[1] >= 21:
            return (0, 1)

        wins = (0, 0)
        places_og = places.copy()
        scores_og = scores.copy()
        # For each possible sum of dice
        # Separate universe (use recursion)
        for roll, nb_occ in self.dice:
            # Update place and score
            places, scores = self.step(places_og, scores_og, turn % 2, roll)
            # Play next step
            w1, w2 = self.stepp(places, scores, turn + 1)
            # print(' ' * turn + f'{roll} {places} {scores} {[w1, w2]}')
            wins = (wins[0] + w1, wins[1] + w2)

        # Now we now that from this configuration the result is wins
        self.rules[key] = wins
        return wins

    def _solve(self, inp_):
        places = self.pre_treat(inp_)
        scores = [0, 0]
        w1, w2 = self.stepp(places, scores)
        print(len(self.rules))
        print(w1, w2)
        return max(w1, w2)


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
