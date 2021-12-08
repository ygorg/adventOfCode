import itertools

with open('03_12_input.txt') as f:
    input_ = f.read()

examples = {'4': 5, '11': 23, '59': 122}


class SpiralMatrix:

    def __init__(self):
        self.container = dict()
        self.__set__(0, 0, 1)

    def __get__(self, x, y):
        try:
            return self.container[x][y]
        except KeyError:
            return 0

    def __set__(self, x, y, val):
        if x not in self.container:
            self.container[x] = dict()
        self.container[x][y] = val

    def _neighboorhood_indexes(self, x, y):
        x_candidates = itertools.product([x], [-1, 0, 1])
        y_candidates = itertools.product([y], [-1, 0, 1])
        product = itertools.product(x_candidates, y_candidates)
        return set([(a + m, b + n) for (a, m), (b, n) in product]) - set([(x, y)])

    def _neighboorhood(self, x, y):
        indexes = self._neighboorhood_indexes(x, y)
        return {(x, y): self.__get__(x, y) for x, y in indexes}

    def _next_index(self, x, y, position):
        if x == y == 0:
            return (x + 1, y), 'r'

        if position == 'b':
            if x == -y:
                position = 'r'
            x += 1
        elif position == 'r':
            if x == y:
                position = 't'
                x -= 1
            else:
                y += 1
        elif position == 't':
            if x == -y:
                position = 'l'
                y -= 1
            else:
                x -= 1
        elif position == 'l':
            if x == y:
                position = 'b'
                x += 1
            else:
                y -= 1

        return (x, y), position

    def fill(self, n):
        index, position = (0, 0), 'r'
        last_value = self.__get__(0, 0)
        # print(index, self._neighboorhood(*index))
        while last_value <= n:
            index, position = self._next_index(*index, position)
            neighboorhood = self._neighboorhood(*index)
            # print(index, neighboorhood)
            last_value = sum(neighboorhood.values())
            self.__set__(*index, last_value)
        return self.__get__(*index)

    def print(self):
        x = sorted(self.container.keys())
        y = sorted(set(sum((list(self.container[x_].keys()) for x_ in x), [])))
        res = '\n'.join([' '.join([str(self.__get__(x_, y_)) for y_ in y]) for x_ in x])
        print(res)


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    number = int(str)
    res = SpiralMatrix().fill(number)
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
