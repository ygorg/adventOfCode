import re

with open('07_12_input.txt') as f:
    input_ = f.read()

examples = {"pbga (66)\n\
xhth (57)\n\
ebii (61)\n\
havc (66)\n\
ktlj (57)\n\
fwft (72) -> ktlj, cntj, xhth\n\
qoyq (66)\n\
padx (45) -> pbga, havc, qoyq\n\
tknk (41) -> ugml, padx, fwft\n\
jptl (61)\n\
ugml (68) -> gyxo, ebii, jptl\n\
gyxo (61)\n\
cntj (57)": 'tknk'}


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    nodes = set()
    sub_nodes = set()
    for line in str.split('\n'):
        label, weight, sub_node = re.match(r'(\w+) \((\d+)\)(?: -> (.*)$)?', line).groups()
        nodes |= set([label])
        if sub_node:
            sub_nodes |= set(sub_node.split(', '))
    res = nodes - sub_nodes
    return list(res)[0]


def test_all(examples, fct):
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example.replace('\n', '\\n'), res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    test_all(examples, solver)
    print('Input answer : {}'.format(solver(input_)))
