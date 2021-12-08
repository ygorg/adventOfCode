with open('16_12_input.txt') as f:
    input_ = f.read()
examples = {'s1,x3/4,pe/b': 'baedc'}


# Naive method
# Compute each dance move on the data structure

def str2intlst(str):
    return [int(i) for i in str if i]


def spin(data, args):
    split = int(args)
    return data[-split:] + data[:-split]


def swap(data, index_a, index_b):
    data[index_a], data[index_b] = data[index_b], data[index_a]
    return data


def exchange(data, args):
    args = args.split('/')
    a = int(args[0])
    b = int(args[1])
    return swap(data, a, b)


def partner(data, args):
    a = data.index(args[0])
    b = data.index(args[-1])
    return swap(data, a, b)


def solver(str, number_programs=None):
    if number_programs is None:
        number_programs = 16
    fct = {'s': spin, 'x': exchange, 'p': partner}
    order = [chr(ord('a') + i) for i in range(number_programs)]
    for move in str.split(','):
        # print(move, '\t', ''.join(order), '->', end='')
        order = fct[move[0]](order, move[1:])
        # print(''.join(order))
    return ''.join(order)


def test_all(examples, fct, fct_param=None):
    if fct_param is None:
        fct_param = {}
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example, **fct_param)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example.replace('\n', '\\n'), res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    # test_all(examples, solver, {'number_programs': 5})
    print('Input answer : {}'.format(solver(input_)))
