with open('11_12_input.txt') as f:
    input_ = f.read()

examples = {'ne,ne,ne': 3,
            'ne,ne,sw,sw': 0,
            'ne,ne,s,s': 2,
            'se,sw,se,sw,sw': 3}


dir2coord = {'n': (0, -1), 'ne': (1, -1), 'nw': (-1, 0),
             's': (0, 1), 'se': (1, 0), 'sw': (-1, 1)}


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    path = str.split(',')
    index = (0, 0)
    index = map(sum, zip(*[dir2coord[d] for d in path]))
    return max(index)


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
