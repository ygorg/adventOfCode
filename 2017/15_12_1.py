from progress.bar import Bar
with open('15_12_input.txt') as f:
    input_ = f.read()

examples_generate = {'Generator A starts with 65\nGenerator B starts with 8921': [[1092455, 430625591],
                                                                                  [1181022009, 1233683848],
                                                                                  [245556042, 1431495498],
                                                                                  [1744312007, 137874439],
                                                                                  [1352636452, 285222916]]}
examples_binary = {'Generator A starts with 65\nGenerator B starts with 8921': [['00000000000100001010101101100111', '00011001101010101101001100110111'],
                                                                                ['01000110011001001111011100111001', '01001001100010001000010110001000'],
                                                                                ['00001110101000101110001101001010', '01010101010100101110001101001010'],
                                                                                ['01100111111110000001011011000111', '00001000001101111100110000000111'],
                                                                                ['01010000100111111001100000100100', '00010001000000000010100000000100']]}
examples_min = {'Generator A starts with 65\nGenerator B starts with 8921': 1}
examples = {'Generator A starts with 65\nGenerator B starts with 8921': 588}


def str2intlst(str):
    return [int(i) for i in str if i]


def next_value(old_value, factor):
    return (old_value * factor) % 2147483647


def int2bin(v, zfill=None):
    if type(v) is list:
        return [int2bin(x, zfill) for x in v]
    if zfill is None:
        zfill = 0
    return bin(v)[2:].zfill(zfill)


def solver_min(str, fct, accu, nb_values):
    factor = {'A': 16807, 'B': 48271}

    data = [l.replace('Generator ', '').split(' starts with ') for l in str.split('\n')]
    old_value = {g: int(v) for g, v in data}
    generators = sorted(old_value.keys())

    res = accu
    for i in range(nb_values):
        for g in generators:
            old_value[g] = next_value(old_value[g], factor[g])
            # bin(int(n))[2:][-16:]
        res = fct(res, [old_value[g] for g in generators])
    return res


def solver(str):
    factor = {'A': 16807, 'B': 48271}

    data = [l.replace('Generator ', '').split(' starts with ') for l in str.split('\n')]
    old_value = {g: int(v) for g, v in data}
    generators = sorted(old_value.keys())

    res = 0
    for i in Bar().iter(range(40000000)):
        if i % 1000000 == 0:
            print()
        for g in generators:
            old_value[g] = next_value(old_value[g], factor[g])
        bin_ = int2bin(list(old_value.values()))
        res += all(bin_[-16:] == v[-16:] for v in bin_)
    return res


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
    test_all(examples_generate, solver_min, {'accu': [], 'nb_values': 5, 'fct': lambda accu, x: accu + [x]})
    test_all(examples_binary, solver_min, {'accu': [], 'nb_values': 5, 'fct': lambda accu, x: accu + [int2bin(x, zfill=32)]})
    test_all(examples_min, solver_min, {'accu': 0, 'nb_values': 5, 'fct': lambda accu, x: accu + all(int2bin(x[0])[-16:] == v[-16:] for v in int2bin(x[1:]))})
    test_all(examples, solver)
    print('Input answer : {}'.format(solver(input_)))
