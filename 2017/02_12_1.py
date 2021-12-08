import sys

with open('02_12_input.txt') as f:
    input_ = f.read()

examples = {"5 1 9 5\n7 5 3\n2 4 6 8": 18}


def str2intlst(str):
    return [int(i) for i in str if i]


def max_min(lst):
    min_ = sys.maxsize
    max_ = - (sys.maxsize - 1)
    for i in lst:
        min_ = i if i < min_ else min_
        max_ = i if i > max_ else max_
    return max_, min_


def solver(str):
    lst = [str2intlst(line.strip().split(' ')) for line in str.strip().split('\n')]
    res = 0
    for line in lst:
        max_, min_ = max_min(line)
        res += max_ - min_
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
