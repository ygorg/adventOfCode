from knot_hash import knot_hash

with open('10_12_input.txt') as f:
    input_ = f.read()

examples = {'': 'a2582a3a0e66e6e86e3812dcb672a272',
            'AoC 2017': '33efeb34ea91902bb2f59c9920caa6cd',
            '1,2,3': '3efbe78a8d82f29979031a4aa0b16a9d',
            '1,2,4': '63960835bcdc130f0b66d7ff4f6a5a8e'}


def solver(str):
    return knot_hash(str)


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
