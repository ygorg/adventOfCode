import re
from collections import Counter

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
cntj (57)": 60}


def str2intlst(str):
    return [int(i) for i in str if i]


def list_items_are_equal(lst):
    return not lst or lst.count(lst[0]) == len(lst)


class Node():
    """docstring for node"""
    def __init__(self, weight, childs):
        self.weight = weight
        self.childs = childs
        self.total_weight = None


class Tower():
    """docstring for Tower"""
    def __init__(self, str):
        self.tower = dict()
        childs = set()
        for line in str.split('\n'):
            label, weight, sub_nodes = re.match(r'(\w+) \((\d+)\)(?: -> (.*)$)?', line).groups()
            try:
                sub_nodes = sub_nodes.split(', ')
                childs |= set(sub_nodes)
            except AttributeError:
                sub_nodes = []
            self.tower[label] = Node(int(weight), sub_nodes)
        self.root = list(set(self.tower.keys()) - childs)[0]

    def traverse(self, label, action):
        node = self.tower[label]
        action(label, node)
        if node is not None:
            for sub in node.childs:
                self.traverse(sub, action)

    def fold(self, label, action, op, dflt_accu):
        def _fold(self, label):
            node = self.tower[label]
            accu = op(dflt_accu, action(label, node))

            if node is not None:
                for sub in node.childs:
                    accu = op(accu, _fold(self, sub))
            return accu
        return _fold(self, label)

    def weight(self, label):
        """
            This implementation is not as readable as the one using fold
            but this implementation keep tracks of what value were
            already computed so it is more efficient
        """
        node = self.tower[label]
        if not node.total_weight:
            w = 0
            for sub in node.childs:
                w += self.weight(sub)
            node.total_weight = node.weight + w
        return node.total_weight

    """
    def weight(self, label):
        return tower.fold(label,
                   (lambda l, n: n.weight),
                   (lambda a, b: a + b),
                   0)
    """

    def unbalanced(self, label):
        node = self.tower[label]
        return not list_items_are_equal([self.weight(sub) for sub in node.childs])

    def balance(self, label):
        print(label)
        node = self.tower[label]
        childs = [self.tower[sub] for sub in node.childs]
        childs_weight = [c.total_weight for c in childs]

        count = Counter(childs_weight)
        majo = max(count, key=count.get)
        mino = min(count, key=count.get)
        mino_index = childs_weight.index(mino)
        childs[mino_index].weight += majo - mino
        return childs[mino_index].weight


def solver(str):
    tower = Tower(str)
    return tower.fold(tower.root,
                      (lambda l, n: tower.balance(l) if tower.unbalanced(l) else None),
                      (lambda a, b: b if b else a if a else None),
                      None)


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
