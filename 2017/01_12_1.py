with open('01_12_input.txt') as f:
    input_ = f.read()

examples = {"1122": 3, "1111": 4, '1234': 0, "91212129": 9}


def str2intlst(str):
    return [int(i) for i in str]


def solver(str):
    lst = str2intlst(str)
    res = 0
    for i in range(-1, len(lst) - 1):
        if lst[i] == lst[i + 1]:
            res += lst[i]
    return res


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
