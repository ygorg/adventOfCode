knot_hash = __import__('10_12_2')
knot_hash = knot_hash.knot_hash

with open('14_12_input.txt') as f:
    input_ = f.read()

examples = {'flqrgnkx': 8108}
examples_min = {'flqrgnkx': '##.#.#..\n.#.#.#.#\n....#.#.\n#.#.##.#\n.##.#...\n##..#..#\n.#...#..\n##.#.##.\n'}


def str2intlst(str):
    return [int(i) for i in str if i]


def hex2bin(hex):
    return bin(int(hex, 16))[2:].zfill((len(hex)) * 4)


def solver_min(str):
    res = ''
    for i in range(8):
        seed = '{}-{}'.format(str, i)
        print(seed)
        hash_ = knot_hash(seed)
        print(hash_)
        line = hex2bin(hash_)
        line = line[:8].replace('0', '.').replace('1', '#') + '\n'
        res += line
    return res


def solver(str):
    res = 0
    for i in range(128):
        seed = '{}-{}'.format(str, i)
        hash_ = knot_hash(seed)
        res += sum(str2intlst(hex2bin(hash_)))
    return res


def test_all(examples, fct):
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example.replace('\n', '\\n'), res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    test_all(examples_min, solver_min)
    test_all(examples, solver)
    print('Input answer : {}'.format(solver(input_)))
