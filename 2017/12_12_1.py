with open('12_12_input.txt') as f:
    input_ = f.read()

examples = {'0 <-> 2\n\
1 <-> 1\n\
2 <-> 0, 3, 4\n\
3 <-> 2, 4\n\
4 <-> 2, 3, 6\n\
5 <-> 6\n\
6 <-> 4, 5': 6}


def str2intlst(str):
    return [int(i) for i in str if i]


def traverse(node, seen_nodes, data):
    for neighbour in data[node]:
        if neighbour in seen_nodes:
            continue
        seen_nodes.add(neighbour)
        seen_nodes = traverse(neighbour, seen_nodes, data)
    return seen_nodes


def solver(str):
    data = [line.split(' <-> ') for line in str.split('\n')]
    data = {int(n[0]): str2intlst(n[1].split(', ')) for n in data}
    accessible = traverse(0, set(), data)
    print(accessible)
    return len(accessible)


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
