import logging
from base import Base
from collections import Counter, defaultdict
from tqdm import tqdm


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'NNCB\n\nCH -> B\nHH -> N\nCB -> H\nNH -> C\nHB -> C\nHC -> B\nHN -> C\nNN -> C\nBH -> H\nNC -> B\nNB -> B\nBN -> B\nBB -> N\nBC -> B\nCC -> N\nCN -> C': 1588
        }

    def pre_treat(self, inp_):
        inp_ = [l.split(' -> ') for l in inp_.split('\n') if l]
        return inp_[0][0], {l[0]: l[1] for l in inp_[1:]}

    def step(self, template, rules):
        # Brute force method: construct the new template by adding every new char
        for i in range(len(template)-2, -1, -1):
            template = template[:i+1] + rules[template[i:i+2]] + template[i+1:]
        return template

    def compute_score(self, template):
        c = Counter(template)
        return max(c.values()) - min(c.values())

    def _solve(self, inp_):
        template, rules = self.pre_treat(inp_)
        for i in range(10):
            template = self.step(template, rules)
        return self.compute_score(template)


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'NNCB\n\nCH -> B\nHH -> N\nCB -> H\nNH -> C\nHB -> C\nHC -> B\nHN -> C\nNN -> C\nBH -> H\nNC -> B\nNB -> B\nBN -> B\nBB -> N\nBC -> B\nCC -> N\nCN -> C': 2188189693529
        }

    def pre_treat(self, inp_):
        # Consider the template as the frequency of 2-grams
        template, rules = super(Second, self).pre_treat(inp_)
        return Counter(template[i:i+2] for i in  range(len(template)-1)), rules

    def step(self, template, rules):
        # Create a new template by applying the rules for every 2-gram and couting resulting new 2-grams
        c = defaultdict(lambda: 0)
        for k, v in template.items():
            # For each different 2-grams `ab`, it will add `v` 2-grams `ax` and `xb`
            c[k[0]+rules[k]] += v
            c[rules[k]+k[1]] += v
        return c

    def compute_score(self, template):
        all_char = set((c for t in template.keys() for c in t))
        c = defaultdict(lambda: 0)
        for k in all_char:
            # Unsure why it has to be the max? Maybe if the char is at first or last position ??
            # But if theres 10 `aX` and 10 `Xb` then there's actually only 10 `X` because they are next to each other
            c[k] = max(sum([template[c+k] for c in all_char]), sum([template[k+c] for c in all_char]))
        return max(c.values()) - min(c.values())

    def _solve(self, inp_):
        template, rules = self.pre_treat(inp_)
        for i in range(40):
            template = self.step(template, rules)
        return self.compute_score(template)


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
