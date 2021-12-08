import itertools

with open('02_12_input.txt') as f:
    input_ = f.read()

examples = {"5 9 2 8": 4, "9 4 7 3": 3, "3 8 6 5": 2, "5 9 2 8\n9 4 7 3\n3 8 6 5": 9}


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    lst = [str2intlst(line.strip().split(' ')) for line in str.strip().split('\n')]
    res = 0
    for line in lst:
        res += max([a / b for a, b in itertools.permutations(line, 2) if a % b == 0] + [1])
    return int(res)


def test_all():
    valid_example = 0
    for example, solution in examples.items():
        res = solver(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example, res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    test_all()
    print('Input answer : {}'.format(solver(input_)))
