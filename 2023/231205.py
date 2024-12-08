import logging
from base import Base

class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""": 35
        }

    def pre_treat(self, inp_):
        inp_ = inp_.split('\n\n')
        seeds = [int(e) for e in inp_[0].split(': ')[-1].split(' ') if e.strip()]
        maps = []
        for m in inp_[1:]:
            m = m.split('\n')
            maps.append((
                # Name of the map
                m[0][:-5].split('-')[-1],
                # Rules
                [[int(e) for e in rule.split(' ') if e.strip()]
                 for rule in m[1:] if rule.strip()]
            ))

        # A map's rule is [begin range, end range, difference]
        maps = [
            (name, [(f, f+l, t-f) for t, f, l in rules])
            for name, rules in maps
        ]
        # Sort each map so the ranges beginning are increasing
        maps = [(n, sorted(rules, key=lambda x: x[0])) for n, rules in maps]
        return seeds, maps

    def apply(self, n: int, rules: list[tuple[int, int, int]]):
        for b, e, diff in rules:
            if b <= n and n < e:
                # If n is the range of the rule
                return n + diff
        # n was in no rule
        return n

    def resolve(self, seed, maps):
        # For every map update the seed
        for name, rules in maps:
            seed = self.apply(seed, rules)
        return seed

    def _solve(self, inp_):
        seeds, maps = self.pre_treat(inp_)
        res = [self.resolve(s, maps) for s in seeds]
        return min(res)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            """seeds: 79 14 54 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4""": 46
        }

    def pre_treat(self, inp_):
        from more_itertools import batched
        seeds, maps = super().pre_treat(inp_)
        # Seed is a list of ranges [begin, end]
        seeds = [(f, f+l) for f, l in batched(seeds, 2)]
        return seeds, maps

    def split_rng(self, rng: tuple[int, int], rule: tuple[int, int, int]):

        b, m, a = None, None, None

        if rng[0] < rule[0]:
            # If rule does not cover the beginning of the range
            b = (rng[0], rule[0])

        if rng[1] > rule[1]:
            # If rule does not cover the end of the range
            a = (rule[1], rng[1])

        # The overlapping part of the rule and the range
        # + add rule[2] for the actual mapping part
        m = (max(rng[0], rule[0]) + rule[2], min(rng[1], rule[1]) + rule[2])

        return b, m, a

        """
        tests = {
            ((2, 7), (0, 4, 10)): (None, (12, 14), (4, 7)),  # overlapping at the end
            ((2, 7), (5, 10, 10)): ((2, 5), (15, 17), None),  # overlapping at the beginning
            ((2, 7), (0, 10, 10)): (None, (12, 17), None),   # overlapping inside
            ((2, 7), (4, 5, 10)): ((2, 4), (14, 15), (5, 7)),  # overlapping outside
        }
        """

    def apply_rules(self, rng, rules, name=None):

        rule_is_before_range = lambda rng, rule: rule[1] <= rng[0]
        range_is_before_rule = lambda rng, rule: rng[1] <= rule[0]

        new_rng = []
        while rng and rules:
            if rule_is_before_range(rng[0], rules[0]):
                # We've move past the rule
                rules.pop(0)
                continue
            if range_is_before_rule(rng[0], rules[0]):
                # We've move past the range
                new_rng.append(rng.pop(0))
                continue

            # There's an overlap
            b, m, a = self.split_rng(rng.pop(0), rules[0])
            if b:
                new_rng.append(b)  # The untouched part
            if m:
                new_rng.append(m)  # The modified part
            if a:
                rng.insert(0, a)  # Maybe this next part will overlap with the next rules

        return new_rng + rng  # Keep the ranges after the last rule

    def _solve(self, inp_):
        seeds, maps = self.pre_treat(inp_)
        seeds = sorted(seeds, key=lambda x: x[0])
        # print("seeds", [(r[0], r[1]) for r in seeds])

        for name, rules in maps:

            # print("    Rules", [(r[0], r[1], r[2]) for r in rules])
            seeds = self.apply_rules(seeds, rules, name=name)
            seeds = sorted(seeds, key=lambda x: x[0])

            # Merge contiguous ranges
            # [(45, 50), (50, 55)] -> [(45, 55)]
            i = 0
            while i < len(seeds) - 1:
                if seeds[i][1] == seeds[i+1][0]:
                    s = seeds.pop(i)
                    seeds[i] = (s[0], seeds[i][1])
                else:
                    i += 1

            # print(name, [(r[0], r[1]) for r in seeds])
        return min([s[0] for s in seeds])


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
