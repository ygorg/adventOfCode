with open('15_12_input.txt') as f:
    input_ = f.read()
examples = {'': None}


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    return None


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
