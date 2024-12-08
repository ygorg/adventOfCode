import logging
from itertools import groupby

from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47''': 143
        }

    def pre_treat(self, inp_):
        rules, updates = inp_.split('\n\n')
        rules = [list(map(int, l.split('|'))) for l in rules.split('\n') if l]
        rules = sorted(rules, key=lambda x: x[0])
        rules = {k: set(e[1] for e in v) for k, v in groupby(rules, lambda x: x[0])}
        manuals = [list(map(int, l.split(','))) for l in updates.split('\n') if l]
        return rules, manuals

    def _solve(self, inp_):
        rules, manuals = self.pre_treat(inp_)
        res = 0
        for m in manuals:
            if all(set(m[:i]) & rules.get(page, set()) == set() for i, page in enumerate(m)):
                res += m[int(len(m)/2)]
        return res


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '''47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47''': 123
        }

    def _solve(self, inp_):
        rules, manuals = self.pre_treat(inp_)
        res = 0
        for m in manuals:
            if all(set(m[:i]) & rules.get(page, set()) == set() for i, page in enumerate(m)):
                # If manual is correctly ordered
                continue

            for i in range(len(m)):
                # For each page is a rule not respected ?
                pbms = set(m[:i]) & rules.get(m[i], set())
                if not pbms:
                    continue
                # print(f'in {m}, {m[i]} should be before {pbms}')
                # Of all the pages that should be after this one,
                # find the first that occurs
                other = min(m.index(p) for p in pbms)
                # Insert current page before first that occurs
                m.insert(other, m.pop(i))
                # print('solved !: ', m)

            res += m[int(len(m)/2)]
            print()
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
