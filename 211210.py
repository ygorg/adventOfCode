import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '[({(<(())[]>[[{[]{<()<>>\n[(()[<>])]({[<{<<[]>>(\n{([(<{}[<>[]}>{[]{[(<()>\n(((({<>}<{<{<>}{[]{[]{}\n[[<[([]))<([[{}[[()]]]\n[{[{({}]{}}([{[{{{}}([]\n{<[[]]>}<{[{[{[]{()[[[]\n[<(<(<(<{}))><([]([]()\n<{([([[(<>()){}]>(<<{{\n<{([{{}}[<[[[<>{}]]]>[]]': 26397
        }
        self.opening = {'<': '>', '(': ')', '{': '}', '[': ']'}
        self.scores = {')': 3, ']': 57, '}': 1197, '>': 25137}

    def pre_treat(self, inp_):
        return [l for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        errors = []
        for i, line in enumerate(inp_):
            pile = []
            for c in line:
                if c in self.opening:
                    pile.append(c)
                elif c not in self.opening:
                    if not pile:
                        errors.append(c)
                        break
                    op_c = pile.pop()
                    if c != self.opening[op_c]:
                        errors.append(c)
                        break

        return sum(self.scores[c] for c in errors)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '[({(<(())[]>[[{[]{<()<>>\n[(()[<>])]({[<{<<[]>>(\n{([(<{}[<>[]}>{[]{[(<()>\n(((({<>}<{<{<>}{[]{[]{}\n[[<[([]))<([[{}[[()]]]\n[{[{({}]{}}([{[{{{}}([]\n{<[[]]>}<{[{[{[]{()[[[]\n[<(<(<(<{}))><([]([]()\n<{([([[(<>()){}]>(<<{{\n<{([{{}}[<[[[<>{}]]]>[]]': 288957
        }
        self.scores = {')': 1, ']': 2, '}': 3, '>': 4}

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        cost = []
        for i, line in enumerate(inp_):
            pile = []
            for c in line:
                if c in self.opening:
                    pile.append(c)
                elif c not in self.opening:
                    if not pile:
                        pile = []
                        break
                    op_c = pile.pop()
                    if c != self.opening[op_c]:
                        pile = []
                        break
            if pile:
                acc = 0
                for c in pile[::-1]:
                    c = self.opening[c]
                    acc = acc * 5 + self.scores[c]
                cost.append(acc)

        cost = sorted(cost)
        return cost[len(cost) // 2]


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
