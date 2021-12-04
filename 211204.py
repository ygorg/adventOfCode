import logging
from base import Base
import re
from collections import defaultdict


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1\n\n22 13 17 11  0\n 8  2 23  4 24\n21  9 14 16  7\n 6 10  3 18  5\n 1 12 20 15 19\n\n 3 15  0  2 22\n 9 18 13 17  5\n19  8  7 25 23\n20 11 10 24  4\n14 21 16 12  6\n\n14 21 17 24  4\n10 16 15  9 19\n18  8 23 26 20\n22 11 13  6  5\n 2  0 12  3  7': 4512
        }

    def pre_treat(self, inp_):
        drawn, inp_ = inp_.split('\n', 1)
        drawn = [int(n) for n in drawn.split(',')]
        boards = []
        acc = []
        for l in inp_.split('\n'):
            if not l:
                if acc:
                    boards.append(acc)
                acc = []
            else:
                acc.append([
                    int(n) for n in re.split(r' +', l.strip())
                ])
        if acc:
            boards.append(acc)
        # We are using hashmap to store for each number, it's position in
        # every board
        data = defaultdict(list)
        for i, board in enumerate(boards):
            for j, line in enumerate(board):
                for k, num in enumerate(line):
                    data[num].append((i, j, k))
        return drawn, data, boards


    def _solve(self, inp_):
        drawn, data, boards = self.pre_treat(inp_)
        counter = defaultdict(lambda: defaultdict(int))
        stop = False
        # We are counting how many times a number was drawn in every
        # lines/columns

        for turn, d in enumerate(drawn):
            for i, j, k in data[d]:
                # We add l and c before line and col numbers to prevent having
                # to use 2 different hashmap
                counter[i][f'l{j}'] += 1
                counter[i][f'c{k}'] += 1
                if counter[i][f'l{j}'] == 5 or counter[i][f'c{k}'] == 5:
                    stop = True
                    break
            if stop:
                break
        summm = []
        for n in set(data) - set(drawn[:turn+1]):
            for board_number, _, _ in data[n]:
                if board_number == i:
                    summm.append(n)
        return d * sum(summm)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1\n\n22 13 17 11  0\n 8  2 23  4 24\n21  9 14 16  7\n 6 10  3 18  5\n 1 12 20 15 19\n\n 3 15  0  2 22\n 9 18 13 17  5\n19  8  7 25 23\n20 11 10 24  4\n14 21 16 12  6\n\n14 21 17 24  4\n10 16 15  9 19\n18  8 23 26 20\n22 11 13  6  5\n 2  0 12  3  7': 1924
        }

    def _solve(self, inp_):
        drawn, data, boards = First.pre_treat(self, inp_)
        counter = defaultdict(lambda: defaultdict(int))
        []
        stop = set()
        # We are counting how many times a number was drawn in every
        # lines/columns

        for turn, d in enumerate(drawn):
            for i, j, k in data[d]:
                # We add l and c before line and col numbers to prevent having
                # to use 2 different hashmap
                counter[i][f'l{j}'] += 1
                counter[i][f'c{k}'] += 1
                # We count the number of won boards
                if counter[i][f'l{j}'] == 5 or counter[i][f'c{k}'] == 5:
                    stop |= set([i])
                if len(stop) == len(boards):
                    break
            if len(stop) == len(boards):
                break
        print(drawn[:turn+1])
        print('\n'.join([' '.join([f'{e:2d}' for e in l]) for l in boards[i]]))
        summm = []
        for n in set(data) - set(drawn[:turn+1]):
            for board_number, _, _ in data[n]:
                if board_number == i:
                    summm.append(n)
        return d * sum(summm)


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
