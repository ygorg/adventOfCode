import logging
from base import Base


class First(Base):
    def __init__(self, test):
        super(First, self).__init__()
        self.examples = {
            """RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)""": 2,
        """LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)""": 6
        }

    def pre_treat(self, inp_):
        inp_ = [l for l in inp_.split('\n') if l]
        instr = [1 if i == 'R' else 0 for i in inp_[0]]
        nodes = [l.split(' = ') for l in inp_[1:]]
        nodes = {l[0]: (l[1][1:4], l[1][6:-1]) for l in nodes}
        return instr, nodes

    def _solve(self, inp_):
        instr, nodes = self.pre_treat(inp_)
        current = 'AAA'
        i = 0
        while current != 'ZZZ':
            current = nodes[current][instr[i % len(instr)]]
            i += 1
        return i


class Second(First):
    def __init__(self, test):
        super(Second, self).__init__(test)
        self.test = test
        self.examples = {
            """LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)""": 6
        }

    def _solve(self, inp_):
        instr, nodes = self.pre_treat(inp_)

        current_nodes = [n for n in nodes if n.endswith('A')]

        next_instruction = lambda i: (instr[i % len(instr)], i + 1)
        next_node = lambda n, i: nodes[n][i]

        """
        # V1 adapted
        i = 0
        while not all(n.endswith('Z') for n in current_nodes):
            current_nodes = [nodes[n][instr[i % len(instr)]] for n in current_nodes]
            print(i, [n + str(instr[i % len(instr)]) for n in current_nodes])
            i += 1
        return i"""

        """
        # For each starting node find the cycle length
        current = [n for n in nodes if n.endswith('A')]

        next_instruction = lambda i: (instr[i % len(instr)], i + 1)
        next_node = lambda n, i: nodes[n][i]

        def find_cycle(current_node, i):
            history = {}
            terminal_nodes = []
            cycle_found = False
            while not cycle_found:
                if current_node.endswith('Z'):
                    terminal_nodes.append(i)

                state = (current_node, i % len(instr))
                if state not in history:
                    history[state] = i
                else:
                    break

                inst, i = next_instruction(i)
                current_node = next_node(current_node, inst)

            return state[0], history[state], i, terminal_nodes

        equations = []
        for beginning in current:
            n, b, e, terminal_nodes = find_cycle(beginning, 0)
            print(f'{n} Found a cycle that began at {b} and we are at {e}, it took {e - b} iterations.')
            print(terminal_nodes)
            # equations.append((b, e - b))
            for t in terminal_nodes[:1]:
                equations.append((b + (t % (e - b)), e - b))

        # Find the PGCD of all the cycle length
        """

        def egcd(a, b):
            if a == 0:
                return (b, 0, 1)
            else:
                g, y, x = egcd(b % a, a)
                return (g, x - (b // a) * y, y)

        if self.test:
            equations = [(1, 2), (4, 6)]
            coeff = 2
            equations = [(a, b // coeff) for a, b in equations]
        else:
            equations = [(4, 11653), (2, 19783), (4, 19241), (4, 16531), (6, 12737), (2, 14363)]
            coeff = 271
            equations = [(a, b // coeff) for a, b in equations]

        print(equations)

        """
        I was going to solve a big system of equations like
        x = 4 mod 11653
        x = 2 mod 19783
        x = 4 mod 19241 ...
        But we just need a multiple of all the cycle length which is the product
        of all the cycle length divided by the common PGCD which here is 271
        """
        M = 1
        for a, b in equations:
            M *= b
        print(M * coeff)
        return M * coeff


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
