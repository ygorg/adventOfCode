import logging
from base import Base

#    cbdgef fgaecd
# fdcge agebfd fecdb fabcd
#  be   cgeb
#   edb cfbegad 

# output : fdgacbe cefdb cefbgd gcbe

# 1, 4, 7, 8 : facile de correspondre signal & nbr grâce à la longueur
# je peut connaitre a en faisant set(n2s[7]) - set(n2s[1])


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\nedbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\nfgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\nfbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\naecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\nfgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\ndbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\nbdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\negadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\ngcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce': 26
        }

    def pre_treat(self, inp_):
        return [[e.split(' ') for e in l.split(' | ')]
                for l in inp_.split('\n') if l]

    def _solve(self, inp_):
        inp_ = self.pre_treat(inp_)
        nb_1478 = 0
        for _, output in inp_:
            for o in output:
                if len(o) in [2, 4, 3, 7]:
                    nb_1478 += 1
        return nb_1478

class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.examples = {
            'be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe\nedbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc\nfgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg\nfbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb\naecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea\nfgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb\ndbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe\nbdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef\negadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb\ngcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce': 61229
        }

    def _solve(self, inp_):
        inp_ = First.pre_treat(self, inp_)
        ref = {
            0: 'abcefg', 1: 'cf', 2: 'acdeg',
            3: 'acdfg', 4: 'bcdf', 5: 'abdfg',
            6: 'abdefg', 7: 'acf', 8: 'abcdefg',
            9: 'abcdfg'
        }
        all_seg = set('abcdefg')
        fer = {v: k for k, v in ref.items()}
        ref = {k: set(v) for k, v in ref.items()}
        solutions = []
        for pbm, output in inp_:
            # First, we create a set of rule
            # for example we know that 'be' is 1 ('cf') because it has 2
            # segments so we create a rule ('be', 'cf'), we do that for
            # 1,4,7,8
            rules = []
            for signal in pbm:
                if len(signal) == 2:
                    rules.append((set(signal), ref[1]))
                elif len(signal) == 3:
                    rules.append((set(signal), ref[7]))
                elif len(signal) == 4:
                    rules.append((set(signal), ref[4]))
                elif len(signal) == 7:
                    rules.append((set(signal), ref[8]))

            # We know that 2,3,5 have 5 segments of which 3 are common (top,
            # mid, bottom) if we remove those common segments from input and
            # reference we can create a rule with the remaining segments
            for cluster in [[2, 3, 5], [0, 6, 9]]:
                hyp_signal = [s for s in pbm if len(s) == len(ref[cluster[0]])]
                common = all_seg.intersection(*hyp_signal)
                common_r = all_seg.intersection(*[ref[s] for s in cluster])
                rules.append((
                    set().union(*[set(s) - common for s in hyp_signal]),
                    set().union(*[ref[s] - common_r for s in cluster])
                ))

            rules = sorted(rules, key=lambda x: len(x[0]))

            # Rules simplification
            # I don't think this algorithm would work with another problem,
            # it should be made more general
            i = 1
            while i != len(rules):
                for j in range(i):
                    # For each smaller rules we simplify the actual rule
                    #  if it contains it (we remove the common segments)
                    ris, rir = rules[i]
                    rjs, rjr = rules[j]
                    if rjs.issubset(ris):
                        rules[i] = ((ris - rjs, rir - rjr))

                for j in range(len(rules)):
                    # For every other rule try to infer new rule
                    ris, rir = rules[i]
                    rjs, rjr = rules[j]
                    # If the rules have 1 different digit and have the same
                    # length we can simplify those two rules by removing the
                    # common segments and we are left with a rule that is the
                    # two common parts
                    if len(ris) > 1 and len(ris) == len(rjs)\
                        and len(ris & rjs) == len(ris) - 1:
                        common = ris & rjs
                        common_r = rir & rjr
                        rules.append((common, common_r))
                        rules[i] = (ris - common, rir - common_r)
                        rules[j] = (rjs - common, rjr - common_r)

                # Sort the rules
                rules = sorted(rules, key=lambda x: len(x[0]))
                i += 1

            # Verify that every segment was identifies
            for a, b in rules:
                assert len(a) == 1 and len(b) == 1
            # Translate the outputs
            rules = {list(k)[0]: list(v)[0] for k, v in rules}
            sortjoin = lambda x: ''.join(sorted(x))
            translated = [sortjoin(rules[c] for c in o) for o in output]
            solutions.append(int(''.join(str(fer[t]) for t in translated)))
        return sum(solutions)


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
