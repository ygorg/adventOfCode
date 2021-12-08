from knot_hash import sparse_knot_hash

with open('10_12_input.txt') as f:
    input_ = f.read()

examples = {'3,4,1,5': 12}


def str2intlst(str):
    return [int(i) for i in str if i]


def solver(str):
    global HASH_LEN
    data = str2intlst(str.split(','))
    hash_ = sparse_knot_hash(data, hash_len=HASH_LEN, nb_round=1, pre_treat_str=lambda x: x)
    return hash_[0] * hash_[1]


def test_all(examples, fct):
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example)
        valid_example += 1 if res == solution else 0
        print('{} -> {} : {} {}'.format(example.replace('\n', '\\n'), res, solution, 'O' if res == solution else 'X'))

    print('{}/{} good answer'.format(valid_example, len(examples)))


if __name__ == '__main__':
    HASH_LEN = 5
    test_all(examples, solver)
    HASH_LEN = None
    print('Input answer : {}'.format(solver(input_)))
