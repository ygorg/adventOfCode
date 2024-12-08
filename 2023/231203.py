import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..''': 4361
        }

    def pre_treat(self, inp_):
        return [l for l in inp_.split('\n') if l]

    def number_at(self, string, i):
        # Given an indice in a string
        # Expand right and left to find all the digits
        # surrounding this position
        b, e = i, i
        while b >= 0 and string[b].isnumeric():
            b -= 1
        b += 1
        while e < len(string) and string[e].isnumeric():
            e += 1
        return b, e, string[b:e]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        part_number = 0
        for i in range(len(inp_)):
            j = 0
            while j < len(inp_[i]):
                if not inp_[i][j].isnumeric():
                    j += 1
                    continue

                # Found a number between b and e
                b, e, nb = self.number_at(inp_[i], j)
                k = len(nb)

                # If any character around is a symbol
                if any(inp_[ii][jj] != '.' and not inp_[ii][jj].isnumeric()
                        for jj in range(max(0, j-1), min(j+k+1, len(inp_[i])))
                        for ii in range(max(0, i-1), min(i+2, len(inp_)))):
                    # Add the part number
                    part_number += int(nb)
                j += k
        return part_number


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '''467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..''': 467835
        }

    def _solve(self, inp_):
        # Really hacky not very proud of this one ...

        inp_ = self.pre_treat(inp_)
        part_number = 0
        for i in range(len(inp_)):
            j = 0
            while j < len(inp_[i]):
                if not inp_[i][j] == '*':
                    j += 1
                    continue

                # If a star is found
                # Check all nine positions around the star for numbers

                numbers = [
                    self.number_at(inp_[ii], jj)
                    for jj in range(max(0, j-1), min(j+2, len(inp_[i])))
                    for ii in range(max(0, i-1), min(i+2, len(inp_)))
                    if inp_[ii][jj].isnumeric()
                ]
                # There are duplicates if a number spans on multiple searching
                # area. So we remove duplicates
                numbers = set(numbers)

                # If there more or less than 2 part numbers stop
                if len(numbers) != 2:
                    j += 1
                    continue

                # Retrieve the 2 numbers from the data structure
                numbers = list(numbers)
                part_number += int(numbers[0][-1]) * int(numbers[1][-1])
                j += 1
        return part_number


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
