import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            # '.....\n.F-7.\n.|.|.\n.L-J.\n.....': 4,
            '..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...': 8,
            '7-F7-\n.FJ|7\nSJLL7\n|F--J\nLJ.LJ': 8,
        }

    def pre_treat(self, inp_):
        return [l for l in inp_.split('\n') if l]

    def display(self, matrix, to_color):
        from colorama import Fore, Style
        colored_char = lambda c, cc: f'{cc}{c}{Style.RESET_ALL}'
        char_map = {'7': '┐', 'L': '└', 'F': '┌', 'J': '┘', '-': '─', '|': '│', '.': '·'}
        for i in range(len(matrix)):
            tmp = ""
            for j in range(len(matrix[i])):
                c = matrix[i][j]
                c = char_map.get(c, c)
                if c == "S":
                    tmp += colored_char(c, Fore.YELLOW)
                elif (i, j) in to_color:
                    tmp += colored_char(c, Fore.BLUE)
                else:
                    tmp += f"{c}"
            print(tmp)

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        print(inp_)
        directions = {
            "7": (( 1,  0), (0, -1)),
            "F": (( 1,  0), (0,  1)),
            
            "J": ((-1,  0), (0, -1)),
            "L": ((-1,  0), (0,  1)),

            "|": ((-1,  0), (1,  0)),
            "-": (( 0, -1), (0,  1)),

            "S": (( 0, -1), (0,  1), (-1,  0), (1,  0)),
        }

        # Parcours de graphe
        at = lambda p: inp_[p[0]][p[1]]
        neighbours = lambda p: [(p[0]+i, p[1]+j) for i, j in directions[at(p)]]

        # Trouver S
        found = False
        i = 0
        while not found and i < len(inp_):
            j = 0
            while not found and j < len(inp_[i]):
                if at((i, j)) == 'S':
                    found = True
                j += 1
            i += 1

        s_position = (i-1, j-1)
        to_visit = [n for n in neighbours(s_position)
                    if s_position in neighbours(n)]
        visited = [s_position]
        steps = 0
        while to_visit:
            p = to_visit.pop(0)
            visited.append(p)
            if at(p) == '.':
                continue

            steps += 1
            for n in neighbours(p):
                if 0 <= n[0] and n[0] < len(inp_) and 0 <= n[1] and n[1] < len(inp_[0]):
                    if n not in visited:
                        to_visit.append(n)

        self.display(inp_, visited)

        # 6891 too high
        # 6890 right answer !
        # 1192 too low
        return len(visited) // 2


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '': 0
        }

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        pass


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
