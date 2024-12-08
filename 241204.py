import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.directions = [
            (-1, -1), (-1, 0), (-1, 1),
            (0, 1), (0, -1),
            (1, -1), (1, 0), (1, 1)
        ]
        self.examples = {
            '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX''': 18
        }

    def pre_treat(self, inp_):
        return [l for l in inp_.split('\n') if l]

    def search_word(self, i, j, x, y, inp_):
        if j+y*3 >= len(inp_) or j+y*3 < 0 or i+x*3 >= len(inp_[j]) or i+x*3 < 0:
            return False

        for k, c in enumerate('MAS', 1):
            if inp_[j+y*k][i+x*k] != c:
                # print(f'Expected {c}, found {inp_[j+y*k][i+x*k]} at {j+y*k},{i+x*k}')
                return False
        return True

    def all_directions(self, i, j, inp_):

        return sum(
            self.search_word(i, j, x, y, inp_)
            for x, y in self.directions
        )
            
                

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        res = 0
        for j in range(len(inp_)):
            for i in range(len(inp_[j])):
                if inp_[j][i] != 'X':
                    continue
                res += self.all_directions(i, j, inp_)
        return res


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '''MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX''': 9
        }

    def find_cross(self, i, j, inp_):
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        acc = 0
        for x, y in directions:
            if inp_[j+y][i+x] == 'M' and inp_[j+y*-1][i+x*-1] == 'S':
                # Found 1 MAS !
                acc += 1
        return acc == 2
                

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        res = 0
        for j in range(1, len(inp_)-1):
            for i in range(1, len(inp_[j])-1):
                if inp_[j][i] != 'A':
                    continue
                res += self.find_cross(i, j, inp_)
        return res


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
