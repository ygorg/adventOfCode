from math import sqrt

with open('03_12_input.txt') as f:
    input_ = f.read()

examples = {"1": 0, "12": 3, "23": 2, "1024": 31}

examples_coord = {1: (0, 0), 2: (1, 0), 3: (1, 1), 4: (0, 1), 5: (-1, 1),
                  6: (-1, 0), 7: (-1, -1), 8: (0, -1), 9: (1, -1), 10: (2, -1),
                  15: (0, 2), 16: (-1, 2), 25: (2, -2)}


def str2intlst(str):
    return [int(i) for i in str if i]


def len_ring(number):
    v = sqrt(number)
    v = int(v) + 1 if int(v) != v else int(v)
    if v % 2 == 0:
        return v + 1
    else:
        return v


def ring(number):
    return int(len_ring(number) / 2)


def tlbr(number):
    if number <= 1:
        return (0, 0)
    aaa = len_ring(number)
    demi_aaa = int(aaa / 2)
    numberr = -(number - aaa**2) / (aaa - 1)

    # print('\t{}'.format(number))

    x_ = None
    y = None

    tab = [1 if numberr >= x and numberr <= x + 1 else 0 for x in range(4)]
    if number == aaa**2:
        tab[-1] = 1

    # print(tab)

    if tab[0]:
        interval_bas = aaa**2 - 1 * (aaa - 1)
        x_ = (number - interval_bas - demi_aaa)
    if tab[1]:
        interval_bas = aaa**2 - 2 * (aaa - 1)
        y = -(number - interval_bas - demi_aaa)
    if tab[2]:
        interval_bas = aaa**2 - 3 * (aaa - 1)
        x_ = -(number - interval_bas - demi_aaa)
    if tab[3]:
        if number == aaa**2:
            interval_bas = number - 1 * (aaa - 1)
            y = -(number - interval_bas - demi_aaa)
        else:
            interval_bas = aaa**2 - 4 * (aaa - 1)
            y = (number - interval_bas - demi_aaa)

    if x_ is None:
        if sum(tab[1:3]) == 1:
            x_ = -ring(number)
        else:
            x_ = ring(number)
    if y is None:
        if sum(tab[1:3]) == 1:
            y = ring(number)
        else:
            y = -ring(number)

    return x_, y


def solver(str):
    number = int(str)
    x, y = tlbr(number)
    x = x if x > 0 else -x
    y = y if y > 0 else -y
    return x + y


def test_all(examples, fct):
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example, res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':

    test_all(examples_coord, tlbr)

    test_all(examples, solver)
    print('Input answer : {}'.format(solver(input_)))
