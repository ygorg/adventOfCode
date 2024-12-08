import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9''': 2
        }

    def pre_treat(self, inp_):
        return [list(map(int, l.split(' '))) for l in inp_.split('\n') if l]

    def safe(self, report):
        diff = lambda r: all(abs(l) >= 1 and abs(l) <= 3 for l in r)
        incr = lambda r: all(l > 0 for l in r)
        decr = lambda r: all(l < 0 for l in r)
        return diff(report) and (incr(report) or decr(report))


    def _solve(self, inp_):
        reports = self.pre_treat(inp_)
        reports = [[report[i] - report[i-1] for i in range(1, len(report))] for report in reports]
        return sum(self.safe(r) for r in reports)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            '''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9''': 4
        }

    def _solve(self, inp_):
        # Originally tried something smarter but didn't work well (try to find
        #  a culprit level, remove it and see if it made the report safe)
        reports = self.pre_treat(inp_)
        make_diff = lambda r: [r[i] - r[i-1] for i in range(1, len(r))]
        safe = 0
        for r in reports:
            if self.safe(make_diff(r)):
                safe += 1
                continue
            
            for i in range(len(r)):
                if self.safe(make_diff(r[:i] + r[i+1:])):
                    safe += 1
                    break
        return safe



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
