import random
import logging

from progress.bar import Bar

with open('16_12_input.txt') as f:
    input_ = f.read()


logger = logging.get_logger(__file__)
logging.basicConfig(level=logging.DEBUG)

class Naive:
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


    def solver(str, number_programs=None, nb_iter=1):
        if number_programs is None:
            number_programs = 16
        fct = {'s': Naive.spin, 'x': Naive.exchange, 'p': Naive.partner}
        order = [chr(ord('a') + i) for i in range(number_programs)]
        for i in range(nb_iter):
            for move in str.split(','):
                order = fct[move[0]](order, move[1:])
                logger.debug('{}\t -> {}'.format(move, ''.join(order)), end='')
            logger.debug('Iter {}: {}'.format(i, ''.join(order)))
        return ''.join(order)

#########
# Moves #
#########

def swap(data, index_a, index_b):
    data[index_a], data[index_b] = data[index_b], data[index_a]
    return data


exchange = swap
partner = lambda data, arg1, arg2: swap(data, data.index(arg1), data.index(arg2))
shift = lambda data, arg1: data[-arg1:] + data[:-arg1]


#################
# I/O functions #
#################

# Generate random dances

def gen_1(cat, data_len):
    """Generate a dance move of the `cat` move

    [description]
    :param cat: Type of dance move
    :type cat: str
    :param data_len: Number of programs
    :type data_len: int
    :returns: dance move
    :rtype: {str 'list}
    """
    rand_int = lambda: random.randint(0, data_len - 1)
    rand_char = lambda: chr(ord('a') + rand_int())
    rand_int_no0 = lambda: random.randint(1, data_len - 1)
    if cat == 's':
        return '{}{}'.format(cat, rand_int_no0())
    elif cat == 'x':
        return '{}{}/{}'.format(cat, rand_int(), rand_int())
    elif cat == 'p':
        return '{}{}/{}'.format(cat, rand_char(), rand_char())


def gen_n(cat=['s', 'x', 'p'], data_len=16, nb=1):
    """Generate `nb` dance moves choosen in `cat` types

    [description]
    :param cat: Type of dance move to generate
    :type cat: str 'list
    :param data_len: Number of programs
    :type data_len: int
    :param nb: Number of dance move to generate
    :type nb: int
    :returns: list of dance move
    :rtype: {str}
    """
    moves = [gen_1(random.choice(cat), data_len) for _ in range(nb)]
    return ','.join(moves)


def test_all(examples, fct, fct_param=None):
    if fct_param is None:
        fct_param = {}
    valid_example = 0
    for example, solution in examples.items():
        res = fct(example, **fct_param)
        valid_example += 1 if res == solution else 0
        logger.info('{} -> {} : {} {}'.format(example.replace('\n', '\\n'), res, solution, 'O' if res == solution else 'X'))

    logger.info('{}/{} good answer'.format(valid_example, len(examples)))

# L'idée est de factoriser les mouvements
# Et que l'application séquentielle de fonctions soit égal a la combinaison des
# fonctions
# En gros trouver des embrouilles pour être sûr que f o g o g == f o g'
# enfin que les optimisations ne changent pas le résultat final.
# Que les fonctions soient injectives? bijectives? surjectives?

# 1. Grouper les index-based et name-based en gardant l'ordre
# 2. Aggreger les index-based en faisant une map
# 3. Aggreger les name-based en faisant une map


def solve_this_shit(dance, number_programs=16, nb_iter=1, optimize=None):
    # Pre-treat dance
    dance = dance.split(',')
    # Initialize variables to keep track of transformations to apply
    # on the initial string
    # Aggregate a dance into 2 dance moves :
    # - index transformation : reorder elements
    # - name transformation : change an element by another
    index_moves = [i for i in range(number_programs)]
    name_moves = [chr(ord('a') + i) for i in range(number_programs)]
    for move in dance:
        logger.debug(move)
        if move[0] == 's':
            arg = int(move[1:])
            index_moves = index_moves[-arg:] + index_moves[:-arg]
            logger.debug('{} : {} {}'.format(''.join(map(str, index_moves)), index_moves[arg:], index_moves[:arg]))
        elif move[0] == 'x':
            arg1, arg2 = map(lambda x: int(x), move[1:].split('/'))
            index_moves[arg1], index_moves[arg2] = index_moves[arg2], index_moves[arg1]
            logger.debug('{} : {} {}'.format(''.join(map(str, index_moves)), index_moves[arg1], index_moves[arg2]))
        elif move[0] == 'p':
            arg1, arg2 = move[1:].split('/')
            arg1, arg2 = name_moves.index(arg1), name_moves.index(arg2)
            name_moves[arg1], name_moves[arg2] = name_moves[arg2], name_moves[arg1]
            logger.debug('{} : {} {}'.format(''.join(name_moves), name_moves[arg1], name_moves[arg2]))

    name_map = {chr(ord('a') + i): v for i, v in enumerate(name_moves)}
    init = [chr(ord('a') + i) for i in range(number_programs)]
    res = [chr(ord('a') + i) for i in range(number_programs)]

    apply_name = lambda x: [name_map[k] for k in x]
    apply_index = lambda x: [x[k] for k in index_moves]

    def get_period(init, func, max_iter):
        res = init
        for i in range(max_iter):
            res = func(res)
            if res == init:
                return i + 1
        return max_iter + 1

    name_period = get_period(init, apply_name, nb_iter)
    try:
        name_to_apply = nb_iter % name_period
    except ZeroDivisionError:
        name_to_apply = 0

    index_period = get_period(init, apply_index, nb_iter)
    try:
        index_to_apply = nb_iter % index_period
    except ZeroDivisionError:
        index_to_apply = 0

    for i in range(name_to_apply):
        res = apply_name(res)

    for i in range(index_to_apply):
        res = apply_index(res)

    return ''.join(res)


nb_iter = 3
nb_programs = 5

examples = [gen_n(data_len=5, nb=10) for _ in range(5)]
examples = {k: Naive.solver(k, number_programs=nb_programs, nb_iter=nb_iter) for k in examples}

if __name__ == '__main__':
    test_all(examples, solve_this_shit, {'nb_iter': nb_iter, 'number_programs': nb_programs})  # , 'optimize': [('shift', {})]})
    solution = solve_this_shit(input_, nb_iter=1000000000)  # , optimize=optimizations)
    logger.info('Input answer : {}'.format(solution))
